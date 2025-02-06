from TinyAgent.templates.TinyReAct import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from TinyAgent.agents.TinyReact import ReactAgent, ReactPrompt, ReactMemory, ReactOutputParser, ReactTool, ReactLLM
from llama_cpp import Llama
import logging
from duckduckgo_search import DDGS  # For web search
import requests
from bs4 import BeautifulSoup
import math
import os

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

llm = ReactLLM(Llama(model_path="models/Meta-Llama-3.1-8B-Instruct-Q6_K.gguf", n_batch=8000, n_gpu_layers=33, n_ctx=8000, chat_format="llama",  verbose=False))

##########################################
# Tool 1: WebSearch (Fetches & summarizes webpages)
##########################################
class WebSearch(ReactTool):
    def run(self, query: str):
        try:
            # Perform the search using DuckDuckGo
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=5)  # Fetch top 5 results

            if results:
                summaries = []
                for result in results:
                    url = result['href']
                    title = result['title']
                    
                    # Fetch the webpage content
                    response = requests.get(url, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract text content from the webpage (summarize first 3 paragraphs)
                    paragraphs = soup.find_all('p')
                    page_text = ' '.join([para.get_text() for para in paragraphs[:3]])
                    
                    # Limit the summary length to 1500 characters
                    summaries.append(f"**{title}**: {page_text[:1500]}... (full content at {url})")

                return f"Web Search Results for '{query}':\n" + "\n\n".join(summaries)
            else:
                return "No relevant search results found."
        except Exception as e:
            return f"Error fetching and summarizing content: {str(e)}"

    def error(self):
        return "Could not complete the web search."


##########################################
# Tool 2: Calculator (Evaluates arithmetic expressions)
##########################################
def safe_eval(expr: str):
    # Allow only safe math functions and constants from the math module
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    # Compile the expression
    code = compile(expr, "<string>", "eval")
    # Verify that all names used in the expression are allowed
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")
    return eval(code, {"__builtins__": {}}, allowed_names)


class Calculator(ReactTool):
    def run(self, expression: str):
        try:
            result = safe_eval(expression)
            return f"The result of the calculation '{expression}' is: {result}"
        except Exception as e:
            return f"Error in calculation: {str(e)}"

    def error(self):
        return "Could not complete the calculation."


##########################################
# Tool 3: Weather (Fetches current weather for a location)
##########################################
class Weather(ReactTool):
    def run(self, location: str):
        # Ensure you have an API key from OpenWeatherMap stored in your environment as OPENWEATHER_API_KEY
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: OpenWeather API key not found. Please set the 'OPENWEATHER_API_KEY' environment variable."
        
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": api_key, "units": "metric"}
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Current weather in {location}: {description} with a temperature of {temp}°C."
        else:
            return f"Error fetching weather data: {response.text}"

    def error(self):
        return "Could not complete the weather lookup."


##########################################
# Assemble the tools and the agent
##########################################
tools = {
    "web_search": WebSearch(),
    "calculator": Calculator(),
    "weather": Weather()
}

system_prompt = PREFIX + TOOLS + FORMAT_INSTRUCTIONS + SUFFIX
prompt = ReactPrompt(system_prompt)
memory = ReactMemory()
parser = ReactOutputParser()
agent = ReactAgent(prompt, memory, parser, tools, llm)

# Run the agent interactively
while True:
    user_input = input("User: ")
    print("Agent:", agent.invoke(user_input), flush=True)
