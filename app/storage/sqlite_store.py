"""
SQLite-backed store for reflection interaction logs.

Lightweight, zero-dependency storage suitable for single-server deployments.
For multi-server or high-volume scenarios, swap to PostgreSQL or MongoDB
via the BaseStore interface.
"""

from typing import List
from app.storage.base_store import BaseStore


class SQLiteStore(BaseStore):
    """
    SQLite storage backend for interaction logs.
    """

    def __init__(self, db_url: str = "sqlite:///reflection_logs.db"):
        """
        Initialize connection and ensure the interactions table exists.

        Args:
            db_url: SQLite connection string.
        """
        self._db_url = db_url

    async def _ensure_table(self) -> None:
        """
        Create the interactions table if it doesn't exist.
        """
        import aiosqlite
        db_path = self._db_url.replace("sqlite:///", "")
        async with aiosqlite.connect(db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id TEXT PRIMARY KEY,
                    framework TEXT,
                    stage TEXT,
                    prompt_text TEXT,
                    model_version TEXT,
                    provider_used TEXT,
                    latency_ms REAL,
                    cached BOOLEAN,
                    feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def write(self, record: dict) -> None:
        """Insert a new interaction record."""
        import aiosqlite
        db_path = self._db_url.replace("sqlite:///", "")
        async with aiosqlite.connect(db_path) as db:
            # First ensure table exists due to lazy load
            await self._ensure_table()
            await db.execute("""
                INSERT INTO interactions 
                (id, framework, stage, prompt_text, model_version, provider_used, latency_ms, cached, feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("id"),
                record.get("framework"),
                record.get("stage"),
                record.get("prompt_text"),
                record.get("model_version"),
                record.get("provider_used"),
                record.get("latency_ms"),
                record.get("cached", False),
                record.get("feedback")
            ))
            await db.commit()

    async def read(self, filters: dict) -> List[dict]:
        """Query records with optional filtering."""
        return []

    async def update(self, record_id: str, updates: dict) -> None:
        """Update an existing record by request_id."""
        import aiosqlite
        if "feedback" in updates:
            db_path = self._db_url.replace("sqlite:///", "")
            async with aiosqlite.connect(db_path) as db:
                await db.execute("UPDATE interactions SET feedback = ? WHERE id = ?", 
                    (updates["feedback"], record_id))
                await db.commit()
