"""
Application configuration.

All tunables are loaded from environment variables with sensible defaults.
Supports .env files for local development via pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Immutable application settings loaded from environment."""

    # --- Server ---
    app_name: str = "ai-reflection-service"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # --- LLM ---
    llm_provider: str = "local"            # local | ollama | openai | huggingface
    llm_model_name: str = "reflection-v1"
    llm_api_key: Optional[str] = None
    llm_api_base_url: Optional[str] = None
    llm_timeout_seconds: int = 30
    llm_max_tokens: int = 256

    # --- Fallback ---
    fallback_enabled: bool = True
    fallback_provider: str = "rule_based"

    # --- Cache ---
    cache_enabled: bool = False
    cache_ttl_seconds: int = 3600

    # --- Logging ---
    log_level: str = "INFO"
    log_responses: bool = True

    # --- Storage ---
    response_log_db: str = "sqlite:///reflection_logs.db"

    # --- Routing ---
    default_framework: str = "what_so_what"  # gibbs | kolb | what_so_what
    min_age_for_gibbs: int = 12

    model_config = SettingsConfigDict(env_file=".env", env_prefix="REFLECT_")


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
