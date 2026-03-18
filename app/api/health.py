"""
Health check endpoints.

Kubernetes-compatible liveness and readiness probes.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    Liveness probe. Returns 200 if the process is alive.
    """
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check():
    """
    Readiness probe.
    Returns 200 only if the LLM provider is loaded and responsive.
    Returns 503 if the provider is unavailable.
    """
    ...
