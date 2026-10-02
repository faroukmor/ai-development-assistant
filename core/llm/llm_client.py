import ollama
MAX_TOKENS = 32768
class LLMClient:
    def __init__(self,model_name):
        self.model_name = model_name

    def _handle_error(self, e):
        if isinstance(e, ollama.ResponseError):
            if e.status_code == 404:
                raise RuntimeError(
                    f"Model '{self.model_name}' is not installed. "
                    f"Run: ollama pull {self.model_name}"
                ) from e
            raise RuntimeError(f"Ollama request failed: {e.error}") from e
        raise RuntimeError(
            "Could not reach Ollama. Make sure it is running: `ollama serve`"
        ) from e
    
    def _options(self, messages=None):
        # Dynamic context window: big enough for this prompt + answer,
        # small enough to stay fast on CPU. Falls back to MAX_TOKENS.
        num_ctx = MAX_TOKENS
        if messages:
            prompt_chars = sum(len(m.get("content", "")) for m in messages)
            needed = int(prompt_chars / 3.5) + 1024 + 512
            num_ctx = max(8192, min(MAX_TOKENS, needed))
        return {
            "temperature": 0,
            "num_predict": 1024,
            "num_ctx": num_ctx,
        }

    def chat(self,messages):
        try:
            response = ollama.chat(
                model   =self.model_name,
                messages=messages,
                options = self._options(messages)
            )
        except Exception as e:
            self._handle_error(e)
        return response["message"]["content"]

    def chat_stream(self, messages):
        """Yield the answer in chunks. Same errors as ask()."""
        try:
            stream = ollama.chat(
                model   =self.model_name,
                messages=messages,
                options = self._options(messages),
                stream=True
            )
            for part in stream:
                content = part.get("message", {}).get("content", "")
                if content:
                    yield content
        except Exception as e:
            self._handle_error(e)