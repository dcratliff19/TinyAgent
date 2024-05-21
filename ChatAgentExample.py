from TinyAgent.agents.TinyChat import ChatAgent, ChatLLM, ChatMemory, ChatOutputParser, ChatPrompt
from TinyAgent.templates.TinyChat import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from llama_cpp import Llama

#Change this value based on your model and your GPU VRAM pool.
n_gpu_layers = 33 
#Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_batch = 10000  


#Assemble the components of the agent. 
system_template = PREFIX + TOOLS + FORMAT_INSTRUCTIONS + SUFFIX
prompt = ChatPrompt(system_template)
llm = ChatLLM(Llama(model_path="models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf", verbose=False, n_ctx=8000))
memory = ChatMemory()
parser = ChatOutputParser()
agent = ChatAgent(prompt, memory, parser, [], llm)

#Use the agent!
while True:
  print("Agent:", agent.invoke(input("User: ")))
