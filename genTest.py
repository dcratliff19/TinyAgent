from llama_cpp import Llama



llm = Llama(
      model_path="models/Meta-Llama-3-8B-Instruct-Q6_K.gguf" ,n_ctx=8000, verbose=True, temp=0.3, chat_format="chatml-function-calling")

response_format={
    "type": "json_object",
    "schema": {
        "type": "object",
        "properties": {"answer": {"type": "string"}},
        "required": ["answer"],
    },
}

messages=[
        {
            "role": "system",
            "content": "You are TinyAgent, a highly intelligent AI.",
        }
        ]

tools=[{
        "type": "function",
        "function": {
          "name": "UserDetail",
          "parameters": {
            "type": "object",
            "title": "UserDetail",
            "properties": {
              "name": {
                "title": "Name",
                "type": "string"
              },
            
            },
            "required": [ "name" ]
          }
        }
      }]

# while True:

#     messages.append({"role":"user", "content": input("User: ")})

#     ai_msg = ""
#     print("Agent: ", end="")
#     for token in llm.create_chat_completion(messages, stream=True):
#         if 'content' in token['choices'][0]['delta']:
#             print(token['choices'][0]['delta']['content'], end="")
#             ai_msg += token['choices'][0]['delta']['content']
    
#     messages.append({"role":"assistant", "content": ai_msg})
#     print()


print(llm.create_chat_completion(
      messages = [
        {
          "role": "system",
          "content": "Based on the user's request, choose a tool to use."

        },
        {
          "role": "user",
          "content": "Extract the last name from both:Dylan Ratliff | Job Done"
        },

      ],
      tools=[{
        "type": "function",
        "function": {
          "name": "UserLastName",
          "description": "Extract the user last name.",
          "parameters": {
            "type": "object",
            "title": "UserLastName",
            "properties": {
              "name": {
                "title": "Name",
                "type": "string",
                "description": "Last Name"
              },
            
            },
            "required": [ "name" ]
          }
        }
      },
      {
        "type": "function",
        "function": {
          "name": "UserFirstName",
          "description": "Extract the user first name.",
          "parameters": {
            "type": "object",
            "title": "UserFirstName",
            "properties": {
              "name": {
                "title": "Name",
                "type": "string",
                "description": "First Name"
              },
            
            },
            "required": [ "name" ]
          }
        }
      }],
        tool_choice="auto"))