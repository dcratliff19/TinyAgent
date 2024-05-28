from TinyAgent.abstracts.LLM import LLM
class llamaLLM(LLM):

    def __init__(self, llm, stop = ["Observation", "Thought", "assistant"], max_tokens=1000):
        super().__init__(llm, stop, max_tokens)
    
    def query(self, query):
        return self.llm(query, stop = self.stop, max_tokens=self.max_tokens)['choices'][0]['text']