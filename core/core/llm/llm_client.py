import ollama

MODEL_NAME = 'qwen2.5:3b'


class LLMClient:
    def __init__(self):
        pass

    def ask(self,system_prompt, user_prompt):
        messages = [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ]

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": 0,
                "num_predict": 1024
            }
        )
        return response["message"]["content"]












    
    
    