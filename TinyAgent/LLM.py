from abc import ABC, abstractmethod

class LLM(ABC):

    @abstractmethod
    def __init__(self, llm):
        self.llm = llm
    
    def query(self, query):
        return self.llm(query, max_tokens=32000, stop=["Observation:", "User:"])['choices'][0]['text']