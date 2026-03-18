"""
FastAPI application factory.

Assembles the application with routers, middleware, exception handlers,
and startup/shutdown lifecycle hooks.
"""

from fastapi import FastAPI
from app.config import get_settings
from app.api.v1.router import router as v1_router
from app.api.health import router as health_router
from app.exceptions.handlers import register_exception_handlers
from app.logging_.logger import configure_logging


def create_app() -> FastAPI:
    """
    Build and return the FastAPI application.

    - Registers API routers under /api/v1
    - Attaches global exception handlers
    - Configures structured logging
    - Initializes LLM provider on startup via lifespan event
    """
    settings = get_settings()
    configure_logging(level=settings.log_level, debug=settings.debug)

    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    register_exception_handlers(application)

    application.include_router(health_router)
    application.include_router(v1_router)

    @application.on_event("startup")
    async def on_startup():
        """Initialize LLM providers and warm up caches on startup."""
        from app.api.v1.dependencies import get_reflection_engine, get_response_logger
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Initializing Reflection Engine and warming up model...")
        engine = get_reflection_engine()
        
        # Trigger health check to lazy-load model into GPU/RAM
        try:
            health_check = await engine._llm_manager.get_healthy_provider()
            if health_check:
                logger.info(f"Model warmed up successfully: {health_check.provider_name}")
            else:
                logger.warning("No healthy LLM provider found.")
        except Exception as e:
            logger.error(f"Failed to initialize model on startup: {e}")
            
        logger.info("Initializing Request log database...")
        db = get_response_logger()
        # Initialize DB here if we had an init method

    @application.on_event("shutdown")
    async def on_shutdown():
        """Graceful cleanup of resources."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Shutting down Reflection Engine...")

    return application


app = create_app()
