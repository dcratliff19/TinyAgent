from abc import ABC, abstractmethod

class Memory(ABC):

    def __init__(self):

        self.history = list()
    
    @abstractmethod
    def add_user_message(self, message):
        self.history.append(message)

        return True
        
    @abstractmethod
    def add_agent_message(self, message):
        self.history.append(message)
        return True
        