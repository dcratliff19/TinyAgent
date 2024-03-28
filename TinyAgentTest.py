from llama_cpp import Llama
import asyncio
from pywizlight import discovery
from TinyAgent.prompts.tinyReAct import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from TinyExampleAgent import TinyAgent, TinyPrompt, TinyMemory, TinyParser, TinyTool, TinyLLM

LLM_PATH = "models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

class get_devices(TinyTool):
    
    def run(self):

        all_devices = []

        loop = asyncio.get_event_loop()
        bulbs = loop.run_until_complete(discovery.discover_lights(broadcast_space="192.168.0.255"))
        for bulb in bulbs:

            state = loop.run_until_complete(bulbs[0].updateState())
            all_devices.append({"device": bulb, "brightness": state.get_brightness(), "state": state.get_state(), "color_temp": state.get_colortemp(), "color_rbg": state.get_rgb()})

        return "List of all smart devices found - " + str(all_devices)
    
    def error(self):
        return "No smart devices found."



tools = {"get_devices": get_devices()}

llm = TinyLLM(llm=Llama(
      model_path=LLM_PATH,
        n_batch=1000,
        n_gpu_layers=33,
        n_ctx=10000,
        verbose=True))
prompt = TinyPrompt(PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX)
memory = TinyMemory()
parser = TinyParser()
agent = TinyAgent(prompt, memory, parser, tools, llm)

while True:
    prompt = input("User: ")
    response = agent.invoke(prompt)
    print("Agent:",response)
