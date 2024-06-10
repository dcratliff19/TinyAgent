from TinyAgent import Agent, Tool, Message, Memory
from TinyAgent.parsers.jsonOutputParser import jsonOutputParser
from TinyAgent.llms.llamaLLM import llamaLLM
from TinyAgent.prompts.llama3InstructPrompt import llama3InstructPrompt
import json
import logging
##Implements the TinyAgent Library into a ToolAgent. Uses default functionality.
class ReactLLM(llamaLLM):

    def __init__(self, llm):
        super().__init__(llm)
    
    def query(self, query):
        return super().query(query)

class ReactTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self):
        return super().run()
    
    def error(self):
        return super().error()

class ReactMessage(Message):
    
    def __init__(self, role, content):
        super().__init__(role, content)

class ReactMemory(Memory):

    def __init__(self):
        super().__init__()

    def add_agent_message(self, message):
        return super().add_agent_message(message)
    
    def add_user_message(self, message):
        return super().add_user_message(message)
    
    def get_history(self):
        return super().get_history()


class ReactPrompt(llama3InstructPrompt):

    def __init__(self, system_template):
        super().__init__(system_template)
    
    def get_prompt(self, memory):
        return super().get_prompt(memory)
    
    def update_scratch_pad(self, content):
        return super().update_scratch_pad(content)
    
    def reset_scractch_pad(self):
        return super().reset_scractch_pad()
    
class ReactOutputParser(jsonOutputParser):

    def __init__(self):
        return None
    
    def parse(self, s, first, last):
        return super().parse(s, first, last)

        
class ReactAgent(Agent):

    def __init__(self, promptManager, memory, outputParser, tools, llm, max_execution=10):
        super().__init__(promptManager, memory, outputParser, tools, llm, max_execution)
    
    def invoke(self, prompt):
        #Clear the scratch pad
        self.prompt.reset_scractch_pad()
        self.prompt.scratch_pad = self.prompt.agent_template + self.prompt.thought_template

        #Add the prompt memory
        self.memory.add_user_message(Message("user", prompt))
        #Force a thought
        execution_count = 1
        
        #Only allow x amount executions.
        while execution_count < self.max_execution:
            logging.debug(self.prompt.get_prompt(self.memory))
            #Query the language model for a response.
            response = self.llm.query(self.prompt.get_prompt(self.memory))['choices'][0]['text']
            #Update the scratch pad with the response in case it is needed 
            #on another loop.
            logging.debug(response)
            self.prompt.update_scratch_pad(response) 
            try:
                
                logging.debug(response)
                #Use the parser to parse out the json returned
                action_json = json.loads("{" + self.parser.parse(response, "{", "}") + "}")
               
                if action_json["action"] == "Final Answer":

                    self.memory.add_agent_message(Message("agent", action_json['action_input']))
                    return action_json['action_input']
                    
                if action_json["action"] in self.tools:
                    #Call the tool and update the scratch pad with the response.
                    if action_json['action_input']:
                        tool_response = self.tools[action_json["action"]].run(action_json['action_input'])
                    else:
                        tool_response = self.tools[action_json["action"]].run()

                    self.prompt.update_scratch_pad(self.prompt.observation_template + " " + str(tool_response) + self.prompt.thought_template)

            except Exception as e:
                self.prompt.update_scratch_pad(self.prompt.observation_template + " You response contained the following error: " + str(e)  + self.prompt.thought_template)

            execution_count += 1

        ##Base case. Returns if the loop ends.
        return "I'm sorry, but I couldn't understand your question."


   