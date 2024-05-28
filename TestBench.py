from llama_cpp import Llama
import json

llm = Llama(
      model_path="models/Meta-Llama-3-8B-Instruct-Q6_K.gguf", 
      verbose=True, 
      chat_format='llama-3'
      )


decisionSystemPrompt = """Decide if the user's input needs a tool usage and return true or false in JSON format.
TOOLS AVAILABLE
---------------
$TOOL_NAME $ARGS $DESC
get_devices {} a tool to get all smart devices on the network.
device_state {ip_address, state = False} a tool to control device state. 
---------------\n"""

def decideTool(message_history):
   
    messages = [
        {
            "role": "system",
            "content": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. The assistant calls functions with appropriate input when necessary",
        },
      ]

    messages.extend(message_history)
    llm.chat_format="chatml-function-calling"
    
    response = llm.create_chat_completion(
      messages = messages,
      tools=[{
        "type": "function",
        "function": {
          "name": "getSmartDevices",
          "description": "Returns a list of all smart devices found on the network.",
          "parameters": {}
        }
      }, 
      {
        "type": "function",
        "function": {
          "name": "changeSmartDeviceState",
          "description": "Allows for smart devices to be turned on or off.",
          "parameters": {
            "type": "object",
            "title": "device",
            "properties": {
              "name": {
                "title": "IP Address",
                "type": "string"
              },
              "age": {
                "title": "State",
                "type": "boolean"
              }
            },
            "required": [ "IP Address", "State" ]
          }
        }
      }],
      tool_choice="auto",
      temperature=0.1,
    )

    llm.chat_format="llama-3"
    return response

def decideNeedTool(message_history):    
    messages = [
        {
            "role": "system",
            "content": decisionSystemPrompt,
        },
        
      ]

    messages.extend(message_history)

    response = llm.create_chat_completion(
      messages=messages,
      response_format={
        "type": "json_object",
        "schema": {
            "type": "object",
            "properties": {"tool_needed": {"type": "boolean"}},
            "required": ["tool_needed"],
        },
      },
      
      temperature=0.1)
    

    if json.loads(response["choices"][0]['message']['content'])['tool_needed']:

        tool_needed = decideTool(message_history=message_history)['choices'][0]['message']['content']
        if tool_needed == 'functions.getSmartDevices:':

            return "TOOL USE RESULT (getSmartDevices): Found 1 wizlight at 192.168.0.167"
        if tool_needed == 'functions.changeSmartDeviceState:':

            return "TOOL USE RESULT (changeSmartDeviceState): Device state changed successfully."

    
    
    return False


TinyAgentSystemPrompt =   [{
            "role": "system",
            "content": "You are TinyAgent, a highly intelligent AI. You can help user's with various ",
        }]

messages=[
      
        ]


while True:

    messages.append({"role":"user", "content": input("User: ")})
    need_tool = decideNeedTool(messages)
    if need_tool:
      messages.append({"role":"assistant", "content": need_tool})
    user_msg = TinyAgentSystemPrompt + messages
    
    ai_msg = ""
    print("Agent: ", end="")
    for token in llm.create_chat_completion(user_msg, stream=True, temperature=0.5):
        if 'content' in token['choices'][0]['delta']:
            response_tokens = token['choices'][0]['delta']['content']
            if response_tokens != None:
              print(response_tokens, end="")
              ai_msg += token['choices'][0]['delta']['content']
    
    messages.append({"role":"assistant", "content": ai_msg})
    print()


