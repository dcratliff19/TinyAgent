
from abc import ABC, abstractmethod

class Prompt(ABC):

    def __init__(self, system_template):
        
        self.system_template = system_template
        self.user_template = "\n<|im_start|>user \nUser: "
        self.agent_template = "\n<|im_start|>assistant \nAgent: "
        self.thought_template = "\n<|im_start|>assistant \nThought"
        self.observation_template = "\n<|im_start|>assistant \nObservation"
        self.end_template = "<|im_end|>\n"

        self.prompt = self.system_template
        self.scratch_pad = ""


    @abstractmethod
    def get_prompt(self, memory):
        
        #Combine the messages into one history
        all_history = ""
        for message in memory.history[:10]:
            if message.role == 'user':
                all_history += self.user_template + message.content + self.end_template
            else:
                all_history += self.agent_template + message.content + self.end_template

        return self.prompt + "\n" + all_history + self.scratch_pad
    
    
    @abstractmethod
    def update_scratch_pad(self, content):
        self.scratch_pad += content

    @abstractmethod
    def reset_scractch_pad(self):
        self.scratch_pad = ""
    