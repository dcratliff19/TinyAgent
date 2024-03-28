# TinyAgent
***What is TinyAgent?*** Tiny Agent is a library designed to handle the execution of Large Language models in the traditional [Agent](https://www.promptingguide.ai/research/llm-agents) architecture *without* the complex abstraction of something like langchain. It strives to be lightweight, flexible and well documented. In it's base implementation, TinyAgent uses the [reAct](https://www.promptingguide.ai/techniques/react#how-it-works) prompt engineering method. This results in a "chain-of-thought" to solve each question. 

#### There are 7 main classes that make up TinyAgent
- **Agent** - Handles the execution loop. It's essentially the "main" function.
- **LLM** - Handles the inference of the large language model.
- **Memory** - Handles the chat history using the *Message* class.
- **Message** - Handles user or agent messages. 
- **Parser** - Handles parsing the output of language model.
- **Prompt** - Handles the prompt assembly. 
- **Tool** - Handles execution of tools when a LLM calls upon them.

#### Run the example:
1. Download a model: https://huggingface.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF/blob/main/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf
2. Place the model in the `models/` folder.
3. Update `LLM_PATH` in the TinyAgentTest.py file.
4. Install the python requirements: `python3 -m pip install -r requirements.txt`
5. Install llama_cpp with GPU support: https://michaelriedl.com/2023/09/10/llama2-install-gpu.html
5. Run the example: `python3 TinyAgentTest.py`


# TODO:
- Add in a debug logging functionality. It should be able to be turned on/off with a env variable change.
- Support ChatGPT, Google Claud out of the box.
- Support general chat agents out of the box.
- Change default toolset to something more usable for the average user.