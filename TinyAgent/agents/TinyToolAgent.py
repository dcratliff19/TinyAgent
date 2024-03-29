from TinyAgent import Agent, Prompt, Tool, Message, Memory, Parser, LLM

##Implements the TinyAgent Library into a ToolAgent. Uses default functionality.
class ToolLLM(LLM):

    def __init__(self, llm):
        super().__init__(llm)
    
    def query(self, query):
        return super().query(query)

class ToolTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self):
        return super().run()
    
    def error(self):
        return super().error()

class ToolMessage(Message):
    
    def __init__(self, role, content):
        super().__init__(role, content)

class ToolMemory(Memory):

    def __init__(self):
        super().__init__()

    def add_agent_message(self, message):
        return super().add_agent_message(message)
    
    def add_user_message(self, message):
        return super().add_user_message(message)
    
    def get_history(self):
        return super().get_history()


class ToolPrompt(Prompt):

    def __init__(self, PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX):
        super().__init__(PREFIX, TOOLS, FORMAT_INSTRUCTIONS, SUFFIX)
    
    def get_prompt(self, memory):
        return super().get_prompt(memory)
    
    def update_scratch_pad(self, content):
        return super().update_scratch_pad(content)
    
    def reset_scractch_pad(self):
        return super().reset_scractch_pad()
    
class ToolParser(Parser):

    def __init__(self):
        return None
    
    def json_parse(self, string, first, last):
        return super().json_parse(string, first, last)

    def parse(self, s, first, last):
        return super().parse(s, first, last)

        
class ToolAgent(Agent):

    def __init__(self, promptManager, memory, outputParser, tools, llm, max_execution=5):
        super().__init__(promptManager, memory, outputParser, tools, llm, max_execution)
    
    def invoke(self, prompt):
        return super().invoke(prompt)

   