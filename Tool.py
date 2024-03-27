
from abc import ABC, abstractmethod

class Tool(ABC):
    def __init__(self):
        return None
    
    @abstractmethod
    def run(self):
        
        return "Hello World!"
    
    @abstractmethod
    def error(self):

        return "There has been an error in the use of the hello world tool."
