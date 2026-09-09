import ollama
class LLMClient:
    def __init__(self,model_name):
        self.model_name = model_name

    def ask(self,messages):
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={
                    "temperature": 0,
                    "num_predict": 1024,
                    "num_ctx": 32768
                }
            )
        except ollama.ResponseError as e:
            if e.status_code == 404:
                raise RuntimeError(
                    f"Model '{self.model_name}' is not installed. "
                    f"Run: ollama pull {self.model_name}"
                ) from e
            raise RuntimeError(f"Ollama request failed: {e.error}") from e
        except Exception as e:
            raise RuntimeError(
                "Could not reach Ollama. Make sure it is running: `ollama serve`"
            ) from e
        return response["message"]["content"]