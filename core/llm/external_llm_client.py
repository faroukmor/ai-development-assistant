import json
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"

# Any OpenAI-compatible endpoint works here (OpenAI, OpenRouter, Groq,
# DeepSeek, Mistral, ...). Same contract as LLMClient: ask(messages) -> str.
class ExternalLLMClient:
    def __init__(self, model_name, api_key, base_url=DEFAULT_BASE_URL):
        if not api_key:
            raise RuntimeError("An API key is required for an external model")
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def ask(self, messages):
        payload = json.dumps({
            "model": self.model_name,
            "messages": messages,
            "temperature": 0,
            "max_tokens": 1024,
        }).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise RuntimeError(
                    "The API key was rejected (401). Check AI_ASSISTANT_API_KEY "
                    "or re-enter the key."
                ) from e
            if e.code == 429:
                raise RuntimeError(
                    "The provider rate limit was hit (429). Wait a moment and "
                    "ask again."
                ) from e
            if e.code == 404:
                raise RuntimeError(
                    f"Model '{self.model_name}' was not found on {self.base_url} "
                    "(404). Check the model name."
                ) from e
            raise RuntimeError(
                f"The external model request failed: HTTP {e.code}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Could not reach the external model at {self.base_url}: {e}"
            ) from e

        return result["choices"][0]["message"]["content"]
