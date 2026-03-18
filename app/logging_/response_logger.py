"""
Response logger.

Writes structured interaction records (request, prompt, response, latency,
provider used) to persistent storage for later analysis and model improvement.

Every reflection interaction is logged regardless of outcome.
"""

import logging
from app.storage.base_store import BaseStore

logger = logging.getLogger(__name__)


class ResponseLogger:
    """
    Logs every reflection interaction for audit and analytics.
    """

    def __init__(self, store: BaseStore):
        """
        Args:
            store: Persistent storage backend for interaction records.
        """
        self._store = store

    async def log_interaction(
        self,
        request_id: str,
        framework: str,
        stage: str,
        prompt_text: str,
        model_version: str,
        provider_used: str,
        latency_ms: float,
        cached: bool = False,
    ) -> None:
        """
        Write a complete interaction record to storage.
        """
        try:
            record = {
                "id": request_id,
                "framework": framework,
                "stage": stage,
                "prompt_text": prompt_text,
                "model_version": model_version,
                "provider_used": provider_used,
                "latency_ms": latency_ms,
                "cached": cached,
                "feedback": None
            }
            await self._store.write(record)
        except Exception as e:
            logger.error(f"Failed to log interaction {request_id}: {str(e)}")

    async def log_feedback(self, request_id: str, feedback: str) -> None:
        """
        Attach learner feedback to an existing interaction record.
        """
        try:
            await self._store.update(request_id, {"feedback": feedback})
        except Exception as e:
            logger.error(f"Failed to log feedback for {request_id}: {str(e)}")
