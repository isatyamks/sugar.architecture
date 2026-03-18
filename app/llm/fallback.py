"""
LLM fallback chain manager.

Tries providers in priority order. If all fail, degrades to a rule-based
prompt generator that requires no external service.

The system never returns an error to the learner — it always provides
*some* reflection prompt. This is a core design principle.
"""

import logging
from typing import List, Callable, Tuple
from app.llm.base_provider import BaseLLMProvider
from app.exceptions.handlers import LLMProviderError

logger = logging.getLogger(__name__)


class FallbackManager:
    """
    Manages a chain of LLM providers with graceful degradation.
    """

    def __init__(
        self,
        providers: List[BaseLLMProvider],
        rule_based_fallback: Callable[[str, str], str],
    ):
        """
        Args:
            providers: Ordered list of providers to try (highest priority first).
            rule_based_fallback: A callable(system_prompt, user_prompt) → str
                                 for offline last-resort prompts.
        """
        self._providers = providers
        self._rule_based_fallback = rule_based_fallback

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs,
    ) -> Tuple[str, str]:
        """
        Try each provider in order. Return (response_text, provider_name).

        If all providers fail, call rule_based_fallback and return
        (fallback_text, "rule_based").

        Never raises — always returns a usable prompt.
        """
        for provider in self._providers:
            try:
                response = await provider.generate(
                    system_prompt, user_prompt, **kwargs
                )
                if response:
                    return response, provider.provider_name
            except Exception as e:
                logger.warning(
                    f"Provider {provider.provider_name} failed: {str(e)}. "
                    "Trying next provider in fallback chain."
                )
                
        # All providers failed -> rule based fallback
        logger.error("All LLM providers failed. Executing rule-based fallback.")
        fallback_prompt = self._rule_based_fallback(system_prompt, user_prompt)
        return fallback_prompt, "rule_based"

    async def get_healthy_provider(self) -> BaseLLMProvider | None:
        """
        Return the first provider that passes health_check(), or None.
        Used by the /ready endpoint.
        """
        for provider in self._providers:
            try:
                if await provider.health_check():
                    return provider
            except Exception as e:
                logger.warning(f"Health check failed for {provider.provider_name}: {str(e)}")
        return None
