from TinyAgent.abstracts.LLM import LLM
class llamaLLM(LLM):

    def __init__(self, llm, stop = ["Observation", "Thought"], max_tokens=1000):
        super().__init__(llm, stop, max_tokens)
    
    def query(self, query, **kwargs):

        return self.llm(query, stop = self.stop, max_tokens=self.max_tokens, **kwargs)