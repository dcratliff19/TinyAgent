# TinyAgent
***What is TinyAgent?*** Tiny Agent is a library designed to handle the execution of Large Language models in the traditional [Agent](https://www.promptingguide.ai/research/llm-agents) architecture *without* the complex abstraction of something like langchain. It strives to be lightweight, flexible and well documented. In it's base implementation, TinyAgent uses the [reAct](https://www.promptingguide.ai/techniques/react#how-it-works) prompt engineering method. This results in a "chain-of-thought" to solve each question. 

#### There are 7 main classes that make up TinyAgent
- **Agent** - Handles the execution loop. It's essentially the "main" function.
- **LLM** - Handles the inference of the large language model.
- **Memory** - Handles the chat history using the *Message* class.
- **Message** - Handles user or agent messages. 
- **Parser** - Handles parsing the output of language model.
- **Prompt** - Handles the prompt assembly. 
- **Tool** - Handles execution of tools when a LLM calls upon them.

#### Run the example:
1. Download a model in `.gguf` format. The [Nous-Hermes-2-Mistral-7b-DPO](https://huggingface.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF/blob/main/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf) is a great instruction following model.
2. Place the model in the `models/` folder.
3. Update `LLM_PATH` in the TinyAgentTest.py file.
4. Install the python requirements: `python3 -m pip install -r requirements.txt`
5. Install llama_cpp with GPU support: https://michaelriedl.com/2023/09/10/llama2-install-gpu.html
5. Run the example: `python3 TinyAgentTest.py`


# Agent Examples

### Chat Agent
```python
from TinyAgent.agents.TinyChatAgent import ChatAgent, ChatLLM, ChatMemory, ChatMessage, ChatParser, ChatPrompt, ChatTool
from TinyAgent.prompts.TinyChat import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from llama_cpp import Llama

#Change this value based on your model and your GPU VRAM pool.
n_gpu_layers = 33 
#Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_batch = 1000  

#Create the LLM.
_llm = Llama(
      model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
        n_batch=n_batch,
        n_gpu_layers=n_gpu_layers,
        n_ctx=10000,
        verbose=False)

#Assemble the components of the agent. 
prompt = ChatPrompt(PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX)
llm = ChatLLM(_llm)
memory = ChatMemory()
parser = ChatParser()
agent = ChatAgent(prompt, memory, parser, [], llm)

#Use the agent!
while True:
  print("Agent:", agent.invoke(input("User: ")))

```

### Tool Agent
```python
from TinyAgent.prompts.TinyReAct import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from TinyAgent.agents.TinyToolAgent import ToolAgent, ToolPrompt, ToolMemory, ToolParser, ToolTool, ToolLLM
from pywizlight import discovery
from llama_cpp import Llama
import asyncio

## Create a custom tool!
class get_devices(ToolTool):
    
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

        return "List of all smart devices found - " + str(all_devices)
    
    def error(self):
        return "No smart devices found."



tools = {"get_devices": get_devices()}
#Assemble the components of the agent. 
llm = ToolLLM(Llama(
      model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf",
        n_batch=1000,
        n_gpu_layers=33,
        n_ctx=10000,
        verbose=False))
prompt = ToolPrompt(PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX)
memory = ToolMemory()
parser = ToolParser()
agent = ToolAgent(prompt, memory, parser, tools, llm)

#Use the agent!
while True:
    print("Agent:", agent.invoke(input("User: ")))
```

# TODO:
- Add in a debug logging functionality. It should be able to be turned on/off with a env variable change.
~~- Support ChatGPT, Google Claud out of the box.~~ Nope! TinyAgent has transitioned to a 100% local agent focused project. 😎
- Change default toolset to something more usable for the average user. Weather, Google search and a user input tool.
- Refactor code base so that we can store implementations of different classes in folders. Example: the Agents folder currently stores entire agent implementations. This can be broken down.