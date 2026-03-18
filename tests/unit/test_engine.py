"""
Unit tests for ReflectionEngine.
"""

import pytest
from app.core.engine import ReflectionEngine


class TestReflectionEngine:
    """Tests for the ReflectionEngine orchestrator."""

    def test_generate_returns_reflection_prompt(self, sample_reflection_request):
        """Engine should return a valid ReflectionPrompt for a well-formed request."""
        ...

    def test_generate_uses_framework_override(self, sample_reflection_request):
        """When framework_override is set, engine should use that framework."""
        ...

    def test_generate_handles_empty_history(self, sample_reflection_request):
        """Engine should work correctly with no prior history."""
        ...

    def test_generate_includes_model_version(self, sample_reflection_request):
        """Response should include the model_version from the registry."""
        ...
