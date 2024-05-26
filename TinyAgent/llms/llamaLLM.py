from TinyAgent.abstracts.LLM import LLM
class llamaLLM(LLM):

    def __init__(self, llm, stop = ["Observation"]):
        super().__init__(llm, stop)
    
    def query(self, query):
        return self.llm(query, stop = ["Observation", "Thought", "assistant"], max_tokens=1500)['choices'][0]['text']