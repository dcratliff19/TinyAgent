from TinyAgent.prompts.TinyReAct import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from TinyAgent.agents.TinyTool import ToolAgent, ToolPrompt, ToolMemory, ToolParser, ToolTool, ToolLLM
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
system_prompt = PREFIX + TOOLS + FORMAT_INSTRUCTIONS + SUFFIX
prompt = ToolPrompt(system_prompt)
memory = ToolMemory()
parser = ToolParser()
agent = ToolAgent(prompt, memory, parser, tools, llm)

#Use the agent!
while True:
    print("Agent:", agent.invoke(input("User: ")))