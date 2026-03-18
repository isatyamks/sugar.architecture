"""
Integration tests for API endpoints.

Tests the full request/response cycle through the FastAPI app
using TestClient (no real LLM calls — uses rule-based fallback).
"""

import pytest
from fastapi.testclient import TestClient


class TestReflectEndpoint:
    """Integration tests for POST /api/v1/reflect."""

    def test_valid_request_returns_200(self, client, sample_reflection_request):
        """A well-formed request should return 200 with a ReflectionResponse."""
        ...

    def test_missing_context_returns_422(self, client):
        """Request without 'context' field should return 422 Validation Error."""
        ...

    def test_invalid_framework_override_returns_422(self, client, sample_reflection_request):
        """Invalid framework_override value should return 422."""
        ...

    def test_response_contains_prompt_text(self, client, sample_reflection_request):
        """Response should contain a non-empty prompt_text."""
        ...

    def test_response_contains_framework_used(self, client, sample_reflection_request):
        """Response should indicate which framework was used."""
        ...

    def test_response_contains_model_version(self, client, sample_reflection_request):
        """Response should include the model version string."""
        ...


class TestFeedbackEndpoint:
    """Integration tests for POST /api/v1/reflect/feedback."""

    def test_valid_feedback_returns_200(self, client):
        """Submitting feedback for a known request_id should return 200."""
        ...

    def test_feedback_without_request_id_returns_422(self, client):
        """Missing request_id should return 422."""
        ...


class TestHealthEndpoints:
    """Integration tests for health/readiness probes."""

    def test_health_returns_200(self, client):
        """GET /health should always return 200."""
        ...

    def test_ready_returns_200_when_provider_available(self, client):
        """GET /ready should return 200 when fallback provider is available."""
        ...
