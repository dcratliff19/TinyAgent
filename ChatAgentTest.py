from llama_cpp import Llama
from TinyAgent.agents.TinyChatAgent import ChatAgent, ChatLLM, ChatMemory, ChatMessage, ChatParser, ChatPrompt, ChatTool
from TinyAgent.prompts.TinyChat import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX

#Change this value based on your model and your GPU VRAM pool.
n_gpu_layers = 33 
#Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_batch = 1000  

#Create the LLM.
_llm = Llama(
      model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf",
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
