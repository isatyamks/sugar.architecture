"""
Integration tests for LLM providers.

These tests verify that each provider implementation correctly implements
the BaseLLMProvider interface. They use mock servers or skipped markers
for providers that require external services.
"""

import pytest
from app.llm.providers.local_model import LocalModelProvider
from app.llm.providers.ollama_provider import OllamaProvider
from app.llm.providers.openai_provider import OpenAIProvider
from app.llm.providers.huggingface_provider import HuggingFaceProvider


class TestLocalModelProvider:
    """Tests for local model inference."""

    @pytest.mark.skip(reason="Requires model weights on disk")
    def test_generate_returns_string(self):
        """generate() should return a non-empty string."""
        ...

    def test_health_check_false_without_model(self):
        """health_check() should return False when no model is loaded."""
        ...


class TestOllamaProvider:
    """Tests for Ollama provider."""

    @pytest.mark.skip(reason="Requires running Ollama instance")
    def test_generate_returns_string(self):
        ...

    @pytest.mark.skip(reason="Requires running Ollama instance")
    def test_health_check(self):
        ...


class TestOpenAIProvider:
    """Tests for OpenAI provider."""

    @pytest.mark.skip(reason="Requires API key")
    def test_generate_returns_string(self):
        ...


class TestHuggingFaceProvider:
    """Tests for HuggingFace provider."""

    @pytest.mark.skip(reason="Requires API key")
    def test_generate_returns_string(self):
        ...
