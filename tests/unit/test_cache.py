"""
Unit tests for CacheManager.
"""

import pytest
from app.cache.cache_manager import CacheManager


class TestCacheManager:
    """Tests for the optional caching layer."""

    def test_returns_none_when_disabled(self):
        """When enabled=False, get() should always return None."""
        ...

    def test_set_and_get(self):
        """Should retrieve a previously cached value."""
        ...

    def test_expired_entries_return_none(self):
        """After TTL, get() should return None."""
        ...

    def test_build_key_is_deterministic(self):
        """Same inputs should always produce the same cache key."""
        ...

    def test_build_key_differs_for_different_inputs(self):
        """Different inputs should produce different cache keys."""
        ...
