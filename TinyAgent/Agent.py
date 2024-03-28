import json
from abc import ABC, abstractmethod
from TinyAgent.Message import Message

class Agent(ABC):

    def __init__(self, prompt, memory, parser, tools, llm, max_execution=5):
        
        self.prompt = prompt
        self.memory = memory
        self.parser = parser
        self.tools = tools
        self.llm = llm
        self.max_execution = max_execution

    @abstractmethod
    def invoke(self, prompt):

        #Clear the scratch pad
        self.prompt.reset_scractch_pad()
        #Add the prompt memory
        self.memory.add_user_message(Message("user", prompt))
        #Force a thought
        self.prompt.update_scratch_pad(self.prompt.thought_template + " 1:")
        execution_count = 1
        
        #Only allow x amount executions.
        while execution_count < self.max_execution:

            print(self.prompt.get_prompt(self.memory))
            #Query the language model for a response.
            response = self.llm.query(self.prompt.get_prompt(self.memory))
            #Update the scratch pad with the response in case it is needed 
            #on another loop.
            self.prompt.update_scratch_pad(response)
            print(self.prompt.get_prompt(self.memory))
            try:
                #Use the parser to parse out the json returned
                action_json = json.loads(self.parser.parse(response, "```json", "```"))
                if action_json["action"] == "Final Answer":

                    self.memory.add_agent_message(Message("agent", action_json['action_input']))
                    return action_json['action_input']
                    
                if action_json["action"] in self.tools:
                    #Call the tool and update the scratch pad with the response.
                    tool_response = self.tools[action_json["action"]].run()
                    self.prompt.update_scratch_pad(self.prompt.observation_template + " " + str(execution_count) + ": " + str(tool_response) + self.prompt.thought_template + " " + str(execution_count + 1) + ":")
                
            except Exception as e:
                self.prompt.update_scratch_pad(self.prompt.observation_template + " " + str(execution_count) + ": Your previous response did not contain a valid JSON response. The following error was found - " + str(e) + self.prompt.thought_template + " " + str(execution_count) + ":")
            
            execution_count += 1

        ##Base case. Returns if the loop ends.
        return "I'm sorry, but I couldn't understand your question."

