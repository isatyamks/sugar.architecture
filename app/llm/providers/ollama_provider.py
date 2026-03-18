"""
Ollama API provider.

Communicates with a local or remote Ollama instance via its REST API.
Ollama provides a simple way to run LLMs locally with minimal setup.

Ref: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

from app.llm.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """
    Ollama-backed LLM inference.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama3"):
        """
        Args:
            base_url: Ollama server URL.
            model_name: Name of the model pulled in Ollama (e.g. 'llama3', 'mistral').
        """
        self._base_url = base_url
        self._model_name = model_name

    @property
    def provider_name(self) -> str:
        return "ollama"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a chat completion request to the Ollama API.

        Implementation should:
        1. POST to {base_url}/api/chat
        2. Use messages format: [{"role": "system", ...}, {"role": "user", ...}]
        3. Parse the response and return the assistant's message content
        """
        ...

    async def health_check(self) -> bool:
        """GET {base_url}/api/tags to verify Ollama is running."""
        ...
