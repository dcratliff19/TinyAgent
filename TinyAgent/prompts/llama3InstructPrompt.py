from TinyAgent.abstracts.Prompt import Prompt

class llama3InstructPrompt(Prompt):
    def __init__(self, system_template):

        super().__init__(system_template)

        self.system_template = system_template
        self.user_template = "<|start_header_id|>user<|end_header_id|>\n"
        self.agent_template = "<|start_header_id|>assistant<|end_header_id|>\n"
        self.end_template = "<|eot_id|>\n"
        self.thought_template = "\nThought "
        self.observation_template = "\nObservation "

        self.prompt = self.system_template
        self.scratch_pad = ""

    def get_prompt(self, memory):
        return super().get_prompt(memory)
    
    def update_scratch_pad(self, content):
        return super().update_scratch_pad(content)
    
    def reset_scractch_pad(self):
        return super().reset_scractch_pad()
    