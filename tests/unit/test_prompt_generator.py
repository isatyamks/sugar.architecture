"""
Unit tests for PromptGenerator.
"""

import pytest
from app.core.prompt_generator import PromptGenerator


class TestPromptGenerator:
    """Tests for the adaptive prompt generator."""

    def test_build_prompt_returns_system_and_user_keys(self):
        """Output dict should have 'system' and 'user' keys."""
        ...

    def test_adapt_for_age_simplifies_for_young_learners(self):
        """Prompt for age < 8 should use simpler vocabulary."""
        ...

    def test_adapt_for_age_preserves_for_older_learners(self):
        """Prompt for age > 12 should remain academic."""
        ...

    def test_adapt_for_language_adds_instruction(self):
        """Non-English language should append language instruction."""
        ...

    def test_adapt_for_language_noop_for_english(self):
        """English should not modify the system prompt."""
        ...

    def test_placeholders_are_filled(self):
        """All {title}, {description} etc. placeholders should be replaced."""
        ...
