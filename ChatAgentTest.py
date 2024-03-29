from llama_cpp import Llama
from TinyAgent import Agent, Message, Prompt, LLM, Tool, Memory, Parser
from TinyAgent.agents.TinyChatAgent import ChatAgent, ChatLLM, ChatMemory, ChatMessage, ChatParser, ChatPrompt, ChatTool
from TinyAgent.prompts.tinyChat import PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX
n_gpu_layers = 33  # Change this value based on your model and your GPU VRAM pool.
n_batch = 1000  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

_llm = Llama(
      model_path="/home/dylan/.cache/gpt4all/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
        n_batch=n_batch,
        n_gpu_layers=n_gpu_layers,
        n_ctx=10000,
        verbose=False)


prompt = ChatPrompt(PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX)
llm = ChatLLM(_llm)
memory = ChatMemory()
parser = ChatParser()
agent = ChatAgent(prompt, memory, parser, [], llm)

while True:
  print("Agent:", agent.invoke(input("User: ")))