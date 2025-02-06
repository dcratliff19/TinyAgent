from abc import ABC, abstractmethod

class LLM(ABC):

    def __init__(self, llm, stop = [], max_tokens=1000):
        self.llm = llm
        self.stop = stop
        self.max_tokens = max_tokens
    
    def query(self, query):
        raise NotImplementedError