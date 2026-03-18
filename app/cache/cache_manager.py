"""
Optional caching layer.

Caches LLM responses keyed by (framework, stage, activity_context_hash).
Reduces redundant LLM calls for repeated activity types.

When enabled, identical requests within the TTL window return
cached prompts without invoking the LLM. This is useful for
classroom scenarios where many learners use the same activity.
"""

import hashlib
import time
from typing import Optional


class CacheManager:
    """
    In-memory TTL cache for reflection prompts.

    For multi-server deployments, replace this with a Redis-backed
    implementation sharing the same interface.
    """

    def __init__(self, ttl_seconds: int = 3600, enabled: bool = False):
        """
        Args:
            ttl_seconds: Time-to-live for cached entries in seconds.
            enabled: If False, all operations are no-ops.
        """
        self._ttl = ttl_seconds
        self._enabled = enabled
        self._store: dict[str, tuple[str, float]] = {}  # key → (value, expiry)

    def get(self, cache_key: str) -> Optional[str]:
        """
        Return cached response if valid, or None.

        Automatically evicts expired entries.
        """
        ...

    def set(self, cache_key: str, response: str) -> None:
        """Store response with TTL expiry timestamp."""
        ...

    @staticmethod
    def build_key(framework: str, stage: str, bundle_id: str, title: str) -> str:
        """
        Construct a deterministic cache key from request parameters.

        Uses SHA-256 hash to normalize key length.
        """
        ...
