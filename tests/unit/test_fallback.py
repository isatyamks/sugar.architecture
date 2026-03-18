"""
Unit tests for FallbackManager.
"""

import pytest
from app.llm.fallback import FallbackManager


class TestFallbackManager:
    """Tests for the LLM fallback chain."""

    def test_uses_first_healthy_provider(self):
        """Should use the first provider that succeeds."""
        ...

    def test_falls_back_on_provider_error(self):
        """If first provider fails, should try the next."""
        ...

    def test_uses_rule_based_when_all_fail(self):
        """If all providers fail, should use rule_based_fallback."""
        ...

    def test_returns_provider_name_with_response(self):
        """Return tuple should include which provider was used."""
        ...

    def test_never_raises(self):
        """generate() should never raise, even if everything fails."""
        ...
