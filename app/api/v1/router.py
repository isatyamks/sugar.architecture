"""
v1 API router.

All reflection-related endpoints are mounted under /api/v1.
"""

from fastapi import APIRouter, Depends
from app.api.v1.schemas.request import ReflectionRequest
from app.api.v1.schemas.response import ReflectionResponse
from app.api.v1.dependencies import get_reflection_engine, get_response_logger
from app.core.engine import ReflectionEngine
from app.logging_.response_logger import ResponseLogger

router = APIRouter(prefix="/api/v1", tags=["reflection"])


@router.post("/reflect", response_model=ReflectionResponse)
async def generate_reflection(
    request: ReflectionRequest,
    engine: ReflectionEngine = Depends(get_reflection_engine),
    logger: ResponseLogger = Depends(get_response_logger),
) -> ReflectionResponse:
    """
    Generate a reflection prompt for the given activity context.
    """
    import uuid
    import time
    start_time = time.time()
    
    request_id = str(uuid.uuid4())
    
    prompt = await engine.generate(request)
    
    latency = (time.time() - start_time) * 1000
    
    # Fire and forget logging
    import asyncio
    asyncio.create_task(
        logger.log_interaction(
            request_id=request_id,
            framework=prompt.framework_used,
            stage=prompt.stage,
            prompt_text=prompt.prompt_text,
            model_version=prompt.model_version,
            provider_used=prompt.model_version,
            latency_ms=latency,
            cached=False
        )
    )
    
    return ReflectionResponse(
        request_id=request_id,
        prompt=prompt,
        cached=False
    )


@router.post("/reflect/feedback")
async def submit_feedback(
    request_id: str,
    feedback: str,
    logger: ResponseLogger = Depends(get_response_logger),
):
    """
    Accept optional learner feedback on prompt quality.
    """
    # Just a stub representation for saving the feedback
    import asyncio
    asyncio.create_task(
        logger.log_feedback(request_id=request_id, feedback=feedback)
    )
    return {"status": "ok"}
