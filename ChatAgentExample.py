from TinyAgent.agents.TinyChat import ChatAgent, ChatLLM, ChatMemory, ChatOutputParser, ChatPrompt
from llama_cpp import Llama
import logging

logging.basicConfig(level=logging.INFO)
system_template = """<|start_header_id|>system<|end_header_id|>\n\nYou are TinyAgent, a super intelligent AI with the personality of JARVIS from Iron Man. You are can help user's with a variety of task, or just chat with them.<|eot_id|>"""
#Assemble the components of the agent. 
prompt = ChatPrompt(system_template)
llm = ChatLLM(Llama(model_path="models/Meta-Llama-3-8B-Instruct.Q6_K.gguf", verbose=False, n_ctx=8000))
memory = ChatMemory()
parser = ChatOutputParser()
agent = ChatAgent(prompt, memory, parser, [], llm)

#Use the agent!
while True:
  user_prompt = input("User: ")
  print("Agent: ", end="")
  for token in agent.invoke(user_prompt, stream=True):
    print(token['choices'][0]['text'], end="", flush=True)

  print()
