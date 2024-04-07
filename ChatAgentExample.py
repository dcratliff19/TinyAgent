from TinyAgent.agents.TinyChat import ChatAgent, ChatLLM, ChatMemory, ChatParser, ChatPrompt
from TinyAgent.prompts.TinyChat import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
from llama_cpp import Llama

#Change this value based on your model and your GPU VRAM pool.
n_gpu_layers = 33 
#Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_batch = 10000  


#Assemble the components of the agent. 
system_template = PREFIX + TOOLS + FORMAT_INSTRUCTIONS + SUFFIX
prompt = ChatPrompt(system_template)
llm = ChatLLM(Llama(
        model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf",
        n_batch=n_batch,
        n_gpu_layers=n_gpu_layers,
        n_ctx=10000,
        verbose=False))
memory = ChatMemory()
parser = ChatParser()
agent = ChatAgent(prompt, memory, parser, [], llm)

#Use the agent!
while True:
  print("Agent:", agent.invoke(input("User: ")))
