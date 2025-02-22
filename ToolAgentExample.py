from TinyAgent.templates.TinyReAct import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from TinyAgent.agents.TinyReact import ReactAgent, ReactPrompt, ReactMemory, ReactOutputParser, ReactTool, ReactLLM
from pywizlight import discovery
from llama_cpp import Llama
import asyncio
from googlesearch import search
import bs4
import urllib.request
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

llm = ReactLLM(Llama(model_path="models/Meta-Llama-3-8B-Instruct.Q6_K.gguf", temp=0.1, n_batch=8000, n_gpu_layers=33, n_ctx=8000, verbose=True))

## Create a custom tool!
class get_devices(ReactTool):
    
    def run(self):

        all_devices = []
        loop = asyncio.get_event_loop()
        bulbs = loop.run_until_complete(discovery.discover_lights(broadcast_space="192.168.0.255"))
        for bulb in bulbs:
            
            state = loop.run_until_complete(bulbs[0].updateState())

            all_devices.append({"device": bulb, 
                                "brightness": state.get_brightness(), 
                                "state": state.get_state(), 
                                "color_temp": state.get_colortemp(), 
                                "color_rbg": state.get_rgb()})
            

        return " The get_devices tool found the following devices on the network: " + str(all_devices)

    def error(self):
        return "No smart devices found."


tools = {"get_devices": get_devices()}
#Assemble the components of the agent. 
system_prompt = PREFIX + TOOLS + FORMAT_INSTRUCTIONS + SUFFIX
prompt = ReactPrompt(system_prompt)
memory = ReactMemory()
parser = ReactOutputParser()
agent = ReactAgent(prompt, memory, parser, tools, llm)

#Use the agent!
while True:
    print("Agent:", agent.invoke(input("User: ")), flush=True)