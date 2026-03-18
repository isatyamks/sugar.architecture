"""
Outbound response schemas.

Defines the structure of all API responses returned to the Sugar Shell client.
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.api.v1.schemas.common import ReflectionFramework


class ReflectionPrompt(BaseModel):
    """A single reflection prompt returned to the client."""

    prompt_text: str = Field(
        ..., description="The reflection question to present to the learner"
    )
    framework_used: ReflectionFramework
    stage: str = Field(
        ..., description="Which stage of the framework this prompt addresses"
    )
    model_version: str = Field(
        ..., description="Version identifier of the model that generated this"
    )
    follow_up_hint: Optional[str] = Field(
        None,
        description="Optional hint to guide the learner if they're stuck",
    )


class ReflectionResponse(BaseModel):
    """Wrapper for the /reflect endpoint response."""

    request_id: str
    prompt: ReflectionPrompt
    cached: bool = False


class ErrorResponse(BaseModel):
    """Standardized error response."""

    error_code: str
    message: str
    detail: Optional[str] = None
