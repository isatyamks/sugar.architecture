"""
Global FastAPI exception handlers.

Ensures all errors are returned as structured ErrorResponse objects,
never raw stack traces. Maps domain exceptions to appropriate HTTP status codes.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class LLMProviderError(Exception):
    """
    Raised when an LLM provider fails to generate a response.

    This should be caught by the FallbackManager before it reaches
    the API layer. If it does reach here, all providers have failed
    AND the rule-based fallback also failed (unlikely).
    """

    def __init__(self, provider: str, detail: str = ""):
        self.provider = provider
        self.detail = detail
        super().__init__(f"LLM provider '{provider}' failed: {detail}")


class FrameworkNotFoundError(Exception):
    """
    Raised when a requested reflection framework is not registered.
    """

    def __init__(self, framework: str):
        self.framework = framework
        super().__init__(f"Reflection framework '{framework}' not found")


class ModelVersionNotFoundError(Exception):
    """
    Raised when a requested model version is not in the registry.
    """

    def __init__(self, version_id: str):
        self.version_id = version_id
        super().__init__(f"Model version '{version_id}' not found")


def register_exception_handlers(app: FastAPI) -> None:
    """
    Attach global exception handlers to the FastAPI app.

    Mapping:
    - LLMProviderError → 503 Service Unavailable
    - FrameworkNotFoundError → 400 Bad Request
    - ModelVersionNotFoundError → 404 Not Found
    - Unhandled exceptions → 500 Internal Server Error
    """

    @app.exception_handler(LLMProviderError)
    async def llm_error_handler(request: Request, exc: LLMProviderError):
        logger.error(f"LLM Error: {exc.provider} - {exc.detail}")
        return JSONResponse(
            status_code=503,
            content={"error_code": "LLM_PROVIDER_ERROR", "message": "The AI provider failed to generate a response", "detail": exc.detail}
        )

    @app.exception_handler(FrameworkNotFoundError)
    async def framework_error_handler(request: Request, exc: FrameworkNotFoundError):
        logger.warning(f"Framework Error: {exc.framework}")
        return JSONResponse(
            status_code=400,
            content={"error_code": "FRAMEWORK_NOT_FOUND", "message": f"Reflection framework '{exc.framework}' not found"}
        )

    @app.exception_handler(ModelVersionNotFoundError)
    async def model_version_error_handler(request: Request, exc: ModelVersionNotFoundError):
        logger.warning(f"Model Version Error: {exc.version_id}")
        return JSONResponse(
            status_code=404,
            content={"error_code": "MODEL_VERSION_NOT_FOUND", "message": f"Model version '{exc.version_id}' not found"}
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred while processing the reflection request."}
        )
