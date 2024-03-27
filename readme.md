# TinyAgent
#### What is TinyAgent?
Tiny Agent is a library designed to handle the execution of Large Language models in the traditional "Agent" architecture *without* the complex abstraction of something like langchain. It strives to be lightweight, flexible and well documented. In it's base implementation, TinyAgent uses the "reAct" (https://www.promptingguide.ai/techniques/react#how-it-works) prompt engineering method. This results in a "chain-of-thought" to solve each question. 

There are 7 main classes that make up TinyAgent
- **Agent** - Handles the execution loop. It's essentially the "main" function.
- **LLM** - Handles the inference of the large language model.
- **Memory** - Handles the chat history using the *Message* class.
- **Message** - Handles user or agent messages. 
- **Parser** - Handles parsing the output of language model.
- **Prompt** - Handles the prompt assembly. 