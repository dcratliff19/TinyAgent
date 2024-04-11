from abc import ABC, abstractmethod

class LLM(ABC):

    def __init__(self, llm, stop = ["User:"]):
        self.llm = llm
        self.stop = stop
    
    def query(self, query):
        raise NotImplementedError