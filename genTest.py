from llama_cpp import Llama
llama = Llama("models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf")


tokens = llama.tokenize(b"Heller")
for token in llama.generate(tokens):
    print(llama.detokenize([token]))