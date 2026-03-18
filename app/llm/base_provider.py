"""
Abstract LLM provider interface.

All LLM backends (local, Ollama, OpenAI, HuggingFace) implement this.
This is the seam that enables model swapping without changing any
business logic in the core or API layers.

To add a new provider:
1. Create a new file in app/llm/providers/
2. Subclass BaseLLMProvider
3. Implement generate() and health_check()
4. Register in the fallback chain via dependencies.py
"""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    LLM provider contract.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier for this provider (e.g. 'ollama', 'openai')."""
        ...

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate a text completion.

        Args:
            system_prompt: Instructions for the model persona and behavior.
            user_prompt: The actual reflection prompt to respond to.
            max_tokens: Maximum response length.
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

        Returns:
            Generated text string.

        Raises:
            LLMProviderError: On any provider-specific failure (timeout, auth, etc).
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Return True if the provider is operational and can accept requests.
        Used by the /ready endpoint and the fallback manager.
        """
        ...
