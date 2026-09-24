import json
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"

# Any OpenAI-compatible endpoint works here (OpenAI, OpenRouter, Groq,
# DeepSeek, Mistral, ...). Same contract as LLMClient: ask(messages) -> str.
class AuthError(RuntimeError):
    """The provider rejected the API key (401). A new key fixes it."""


class ExternalLLMClient:
    def __init__(self, model_name, api_key, base_url=DEFAULT_BASE_URL,
                 temperature=0, max_tokens=1024, timeout=120):
        if not api_key:
            raise RuntimeError("An API key is required for an external model")
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def set_api_key(self, api_key):
        """Replace the key in place (e.g. after a 401) without a restart."""
        if not api_key:
            raise RuntimeError("The API key cannot be empty")
        self.api_key = api_key

    def _request(self, messages, stream=False):
        payload = json.dumps({
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }).encode("utf-8")
        return urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

    def _http_error(self, error):
        """Translate an HTTPError into the most actionable message."""
        if error.code == 401:
            return AuthError("The API key was rejected (401). Enter a new key.")
        if error.code == 429:
            return RuntimeError(
                "The provider rate limit was hit (429). Wait a moment and "
                "ask again."
            )
        if error.code == 404:
            return RuntimeError(
                f"Model '{self.model_name}' was not found on {self.base_url} "
                "(404). Check the model name."
            )
        return RuntimeError(f"The external model request failed: HTTP {error.code}")

    def ask(self, messages):
        try:
            with urllib.request.urlopen(self._request(messages), timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise self._http_error(e) from e
        except Exception as e:
            raise RuntimeError(
                f"Could not reach the external model at {self.base_url}: {e}"
            ) from e

        choices = result.get("choices") or []
        if not choices or "message" not in choices[0]:
            raise RuntimeError(
                "The provider response had no message content — nothing to show."
            )
        return choices[0]["message"]["content"]

    def ask_stream(self, messages):
        """Yield the answer incrementally via the provider's SSE stream.

        Same errors as ask(); they surface at the exact moment they happen.
        Malformed lines are skipped, so one odd chunk cannot kill the stream.
        """
        try:
            with urllib.request.urlopen(self._request(messages, stream=True), timeout=self.timeout) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="replace").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[len("data:"):].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = chunk.get("choices") or []
                    if not choices:
                        continue
                    content = (choices[0].get("delta") or {}).get("content")
                    if content:
                        yield content
        except urllib.error.HTTPError as e:
            raise self._http_error(e) from e
        except Exception as e:
            raise RuntimeError(
                f"Could not reach the external model at {self.base_url}: {e}"
            ) from e
