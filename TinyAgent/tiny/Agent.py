from abc import ABC, abstractmethod
from TinyAgent.tiny.Message import Message
import logging
class Agent(ABC):

    def __init__(self, prompt, memory, parser, tools, llm, max_execution=5):
        
        self.prompt = prompt
        self.memory = memory
        self.parser = parser
        self.tools = tools
        self.llm = llm
        self.max_execution = max_execution

    @abstractmethod
    def invoke(self, prompt, **kwargs):

        #Set the scratch pad to the agent template.
        self.prompt.scratch_pad = self.prompt.agent_template
        #Add the user prompt to the memory
        self.memory.add_user_message(Message("user", prompt))
        #Query the language model for a response.
        logging.debug(self.prompt.get_prompt(self.memory))
        
        response = self.llm.query(self.prompt.get_prompt(self.memory), **kwargs)
        #Update the memory with the response in case it is neede
        self.memory.add_user_message(Message("assistant", response))
            
        #return the response.
        return response
