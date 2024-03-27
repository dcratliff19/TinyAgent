import json
from abc import ABC, abstractmethod
from TinyAgent import Message

class Agent(ABC):

    def __init__(self, promptManager, memory, outputParser, tools, llm, max_execution=5):
        
        self.promptManager = promptManager
        self.memory = memory
        self.outputParser = outputParser
        self.tools = tools
        self.llm = llm
        self.max_execution = max_execution

    @abstractmethod
    def invoke(self, prompt):

        self.promptManager.reset_scractch_pad()
        self.memory.add_user_message(Message.Message("user", prompt))
        self.promptManager.update_scractch_pad(self.promptManager.thought_template)
        execution_count = 0

        while execution_count > self.max_execution:

            response = self.llm.query(self.promptManager.get_prompt(self.memory))
            self.promptManager.update_scractch_pad(response)

            try:
                action_json = json.loads(self.outputParser.parse(response, "```json", "```"))
                if action_json["action"] == "Final Answer":

                    self.memory.add_agent_message(Message.Message("agent", action_json['action_input']))
                    return action_json['action_input']
                    
                if action_json["action"] in self.tools:

                    tool_response = self.tools[action_json["action"]].run()
                    self.promptManager.update_scractch_pad("\nObservation (from tool use): " + str(tool_response) + "\nThought: ")
                
            except Exception as e:
                
                self.promptManager.update_scractch_pad("\nObservation (from error): Your previous response did not contain a valid JSON response. The following error was found - " + str(e) + "\nThought: ")
            
            execution_count += 1

        ##Base case. Returns if the loop ends.
        return "I'm sorry, but I couldn't understand your question."

