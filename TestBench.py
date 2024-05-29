from llama_cpp import Llama
import json
import logging

logging.basicConfig(level=logging.INFO)


llm = Llama(
      model_path="models/Meta-Llama-3-8B-Instruct.Q6_K.gguf", 
      verbose=True, 
      n_gpu_layers=33,
      chat_format='chatml-function-calling',
      n_ctx=8200
      )



def decideTool(message_history):
   
    messages = [
        {
            "role": "system",
            "content": "Based on the last user input, call a function.",
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
          "description": "Allows for smart a smart device to be turned on or off.",
          "parameters": {
            "type": "object",
            "title": "device",
            "properties": {
              "ip_address": {
                "title": "IP Address",
                "type": "string"
              },
              "new_state": {
                "title": "State",
                "type": "string"
              }
            },
            "required": [ "IP Address", "State" ]
          }
        }
      }],
      tool_choice="auto",    )

    logging.info(response)

    return response


TinyAgentSystemPrompt =   [{
            "role": "system",
            "content": "You are TinyAgent, a highly intelligent AI. You can help user's with various tasks. ",
        }]

messages=[
      
        ]


while True:

    messages.append({"role":"user", "content": input("User: ")})
    need_tool = decideTool(messages)
    
    if 'tool_calls' in need_tool["choices"][0]['message']:
      tool_needed = need_tool["choices"][0]['message']['tool_calls'][0]['function']['name']
      if tool_needed == 'getSmartDevices':
            logging.info("Using tool get smart devices")

            messages.append({"role":"assistant", "content": "TOOL USE RESULT (getSmartDevices): Found 1 wizlight at 192.168.0.167"})
        
      if tool_needed == 'changeSmartDeviceState':
            logging.info("Using tool change smart devices")
            messages.append({"role":"assistant", "content": "TOOL USE RESULT (changeSmartDeviceState): Device state changed successfully."})


    user_msg = TinyAgentSystemPrompt + messages
    
    ai_msg = ""
    print("Agent: ", end="")
    for token in llm.create_chat_completion(user_msg, stream=True, temperature=0.5):
        if 'content' in token['choices'][0]['delta']:
            response_tokens = token['choices'][0]['delta']['content']
            if response_tokens != None:
              print(response_tokens, end="", flush=True)
              ai_msg += token['choices'][0]['delta']['content']
    
    messages.append({"role":"assistant", "content": ai_msg})
    print()


