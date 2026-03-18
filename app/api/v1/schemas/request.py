"""
Inbound request schemas.

These Pydantic models validate and document the data sent by the Sugar Shell client.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from app.api.v1.schemas.common import ReflectionFramework


class ActivityContext(BaseModel):
    """Contextual information about the activity being reflected upon."""

    activity_id: str = Field(..., description="Sugar activity unique ID")
    bundle_id: str = Field(
        ..., description="Activity bundle identifier (e.g. org.laptop.Write)"
    )
    title: str = Field(..., description="Activity/journal entry title")
    description: Optional[str] = Field(
        None, description="Existing journal description"
    )
    mime_type: Optional[str] = Field(None, description="Content MIME type")
    tags: Optional[List[str]] = Field(default_factory=list)
    buddies: Optional[List[str]] = Field(
        default_factory=list, 
        description="List of IDs or names of collaborating learners in the session"
    )
    duration_seconds: Optional[int] = Field(
        None, description="Time spent in this session"
    )


class LearnerProfile(BaseModel):
    """Minimal learner metadata for prompt routing."""

    age: Optional[int] = Field(None, ge=4, le=99)
    grade_level: Optional[str] = None
    language: str = Field("en", description="ISO 639-1 language code")


class ReflectionRequest(BaseModel):
    """Top-level request body for the /reflect endpoint."""

    context: ActivityContext
    learner: Optional[LearnerProfile] = None
    framework_override: Optional[ReflectionFramework] = Field(
        None,
        description="Force a specific framework instead of auto-routing",
    )
    history: Optional[List[dict]] = Field(
        default_factory=list,
        description="Previous journal entries for continuity-aware prompting",
    )
