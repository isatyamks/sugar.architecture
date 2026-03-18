"""
FastAPI dependency providers.

Lazily instantiates and caches service singletons for injection into route handlers.
These act as the composition root for the application's dependency graph.
"""

from functools import lru_cache
from app.core.engine import ReflectionEngine
from app.core.routing import FrameworkRouter
from app.core.prompt_generator import PromptGenerator
from app.core.frameworks.gibbs import GibbsFramework
from app.core.frameworks.kolb import KolbFramework
from app.core.frameworks.what_so_what import WhatSoWhatFramework
from app.core.frameworks.kwl import KWLFramework
from app.core.frameworks.socratic import SocraticFramework
from app.llm.fallback import FallbackManager
from app.logging_.response_logger import ResponseLogger
from app.storage.sqlite_store import SQLiteStore
from app.config import get_settings
from app.api.v1.schemas.common import ReflectionFramework


@lru_cache()
def get_reflection_engine() -> ReflectionEngine:
    """
    Build and return the configured ReflectionEngine singleton.

    Wires together: FrameworkRouter, PromptGenerator, FallbackManager.
    """
    settings = get_settings()

    frameworks = {
        ReflectionFramework.GIBBS: GibbsFramework(),
        ReflectionFramework.KOLB: KolbFramework(),
        ReflectionFramework.WHAT_SO_WHAT: WhatSoWhatFramework(),
        ReflectionFramework.KWL: KWLFramework(),
        ReflectionFramework.SOCRATIC: SocraticFramework(),
    }

    framework_router = FrameworkRouter(frameworks=frameworks)
    prompt_generator = PromptGenerator()
    llm_manager = _build_fallback_manager(settings)

    return ReflectionEngine(
        router=framework_router,
        prompt_generator=prompt_generator,
        llm_manager=llm_manager,
    )


@lru_cache()
def get_response_logger() -> ResponseLogger:
    """Return the ResponseLogger singleton backed by SQLite."""
    settings = get_settings()
    store = SQLiteStore(db_url=settings.response_log_db)
    return ResponseLogger(store=store)


def _build_fallback_manager(settings) -> FallbackManager:
    """
    Construct the LLM fallback chain from settings.

    Instantiates the primary provider and optional fallback providers.
    Always includes a rule-based fallback as the last resort.
    """
    providers = []

    # Currently we only initialize the local provider. 
    # In a full setup, this would use a factory or switch based on settings.llm_provider
    if settings.llm_provider.lower() == "local":
        from app.llm.providers.local_model import LocalModelProvider
        providers.append(LocalModelProvider(model_path=settings.llm_model_name))
    
    # Offline Last-Resort Rule-Based Generator
    def _rule_based_generator(sys_prompt: str, user_prompt: str) -> str:
        # A simple switch string parsing based on standard stages 
        if "what did you make" in sys_prompt.lower() or "what did you do" in sys_prompt.lower():
            return "What did you make today?"
        if "why does it matter" in sys_prompt.lower() or "what did you learn" in sys_prompt.lower():
            return "What did you learn from doing that?"
        if "what comes next" in sys_prompt.lower() or "try differently" in sys_prompt.lower():
            return "What would you try differently next time?"
        
        # Absolute generic fallback
        return "Can you tell me more about what you just did?"

    return FallbackManager(providers=providers, rule_based_fallback=_rule_based_generator)
