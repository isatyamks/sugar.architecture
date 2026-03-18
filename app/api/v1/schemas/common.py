"""
Shared schema types.

Enums and base types shared across request and response schemas.
"""

from enum import Enum


class ReflectionFramework(str, Enum):
    """Supported reflective practice frameworks."""

    GIBBS = "gibbs"
    KOLB = "kolb"
    WHAT_SO_WHAT = "what_so_what"
    KWL = "kwl"
    SOCRATIC = "socratic"


class LLMProvider(str, Enum):
    """Supported LLM provider backends."""

    LOCAL = "local"
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    RULE_BASED = "rule_based"
