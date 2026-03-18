"""
Abstract base class for reflective practice frameworks.

Each framework defines its stages (phases), stage-specific prompt templates,
and logic for selecting the current stage based on activity context and
learner history.

To add a new framework:
1. Create a new file in this directory.
2. Subclass BaseReflectionFramework.
3. Implement all abstract methods.
4. Register it in app/api/v1/dependencies.py.
"""

from abc import ABC, abstractmethod
from typing import List
from app.api.v1.schemas.request import ActivityContext


class BaseReflectionFramework(ABC):
    """
    Interface contract for all reflection framework implementations.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable framework name."""
        ...

    @property
    @abstractmethod
    def stages(self) -> List[str]:
        """Ordered list of reflection stages/phases."""
        ...

    @abstractmethod
    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Determine which stage of the reflective cycle to prompt for.

        May use activity context and reflection history to decide
        which stage the learner should engage with next.

        Args:
            context: Current activity metadata.
            history: Previous reflection interactions for this activity type.

        Returns:
            Stage name string (must be one of self.stages).
        """
        ...

    @abstractmethod
    def get_system_prompt(self, stage: str) -> str:
        """
        Return the LLM system prompt template for the given stage.

        This guides the LLM's persona, tone, and instructional intent.

        Args:
            stage: One of self.stages.

        Returns:
            System prompt string for the LLM.
        """
        ...

    @abstractmethod
    def get_user_prompt_template(self, stage: str) -> str:
        """
        Return the user-facing prompt template for the given stage.

        Placeholders available: {title}, {description}, {activity_type}, {duration}

        Args:
            stage: One of self.stages.

        Returns:
            User prompt template string with placeholders.
        """
        ...
