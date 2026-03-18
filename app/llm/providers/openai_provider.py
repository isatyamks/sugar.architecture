"""
OpenAI-compatible API provider.

Works with OpenAI, Azure OpenAI, and any API implementing the
OpenAI chat completions spec (e.g. vLLM, LiteLLM, Together AI).
"""

from app.llm.base_provider import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI-compatible chat completions provider.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-3.5-turbo",
        base_url: str | None = None,
    ):
        """
        Args:
            api_key: API key for authentication.
            model_name: Model identifier (e.g. 'gpt-4', 'gpt-3.5-turbo').
            base_url: Optional custom base URL for OpenAI-compatible APIs.
        """
        self._api_key = api_key
        self._model_name = model_name
        self._base_url = base_url or "https://api.openai.com/v1"

    @property
    def provider_name(self) -> str:
        return "openai"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """
        Call the OpenAI chat completions API.

        Implementation should:
        1. POST to {base_url}/chat/completions
        2. Include Authorization header with bearer token
        3. Use messages format with system + user roles
        4. Return choices[0].message.content
        """
        ...

    async def health_check(self) -> bool:
        """Verify the API key is valid by listing models."""
        ...
