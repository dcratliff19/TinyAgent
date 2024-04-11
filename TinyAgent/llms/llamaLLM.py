from TinyAgent import LLM
class llamaLLM(LLM):

    def __init__(self, llm, stop = ["Observation", "User"]):
        super().__init__(llm, stop)
    
    def query(self, query):
        return self.llm(query, max_tokens=32000, stop=self.stop)['choices'][0]['text']