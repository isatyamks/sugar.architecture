"""
Abstract storage interface for the response logger.

To add a new storage backend (e.g. PostgreSQL, MongoDB):
1. Create a new file in this directory.
2. Subclass BaseStore.
3. Implement write(), read(), update().
4. Swap in app/api/v1/dependencies.py.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseStore(ABC):
    """
    Storage contract for interaction log records.
    """

    @abstractmethod
    async def write(self, record: dict) -> None:
        """
        Persist a single interaction record.

        Args:
            record: Dict containing interaction fields (request_id, framework,
                     stage, prompt_text, model_version, provider_used, latency_ms, etc.)
        """
        ...

    @abstractmethod
    async def read(self, filters: dict) -> List[dict]:
        """
        Query interaction records matching the given filters.

        Args:
            filters: Key-value pairs to filter by (e.g. {"framework": "gibbs"}).

        Returns:
            List of matching interaction records.
        """
        ...

    @abstractmethod
    async def update(self, record_id: str, updates: dict) -> None:
        """
        Update an existing record (e.g. to attach feedback).

        Args:
            record_id: The request_id of the record to update.
            updates: Key-value pairs to merge into the record.
        """
        ...
