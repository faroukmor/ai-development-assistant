import ollama




class LLMClient:
    def __init__(self,model_name):
        self.model_name = model_name

    def ask(self,messages):

        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            options={
                "temperature": 0,
                "num_predict": 1024
            }
        )
        return response["message"]["content"]












    
    
    