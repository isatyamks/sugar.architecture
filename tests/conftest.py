"""
Shared pytest fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.config import Settings


@pytest.fixture
def test_settings() -> Settings:
    """
    Return test-specific settings.

    Overrides:
    - Uses rule-based fallback (no real LLM calls)
    - Disables caching
    - Uses in-memory SQLite
    - Sets debug logging
    """
    return Settings(
        debug=True,
        log_level="DEBUG",
        llm_provider="rule_based",
        cache_enabled=False,
        response_log_db="sqlite:///:memory:",
        fallback_enabled=True,
    )


@pytest.fixture
def app(test_settings):
    """Create a FastAPI app with test settings injected."""
    ...


@pytest.fixture
def client(app) -> TestClient:
    """Return a TestClient bound to the test app."""
    return TestClient(app)


@pytest.fixture
def sample_activity_context() -> dict:
    """Return a valid ActivityContext as a dict."""
    return {
        "activity_id": "test-activity-123",
        "bundle_id": "org.laptop.WritetestActivity",
        "title": "My Story About the Ocean",
        "description": "A short story about marine life.",
        "mime_type": "text/plain",
        "tags": ["writing", "science"],
        "duration_seconds": 1200,
    }


@pytest.fixture
def sample_learner_profile() -> dict:
    """Return a valid LearnerProfile as a dict."""
    return {
        "age": 10,
        "grade_level": "5th",
        "language": "en",
    }


@pytest.fixture
def sample_reflection_request(sample_activity_context, sample_learner_profile) -> dict:
    """Return a valid ReflectionRequest as a dict."""
    return {
        "context": sample_activity_context,
        "learner": sample_learner_profile,
        "framework_override": None,
        "history": [],
    }
