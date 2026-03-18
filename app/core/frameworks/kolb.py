"""
Kolb Experiential Learning Cycle implementation.

Stages:
  Concrete Experience → Reflective Observation →
  Abstract Conceptualization → Active Experimentation

Balanced for mid-age learners. Emphasizes the connection between
doing and thinking, encouraging learners to theorize about their
experience and plan experiments.
"""

from typing import List
from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ActivityContext


class KolbFramework(BaseReflectionFramework):
    """
    Kolb's four-stage experiential learning cycle.
    """

    STAGES = [
        "concrete_experience",
        "reflective_observation",
        "abstract_conceptualization",
        "active_experimentation",
    ]

    @property
    def name(self) -> str:
        return "Kolb Experiential Learning Cycle"

    @property
    def stages(self) -> List[str]:
        return self.STAGES

    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Select stage based on history depth.
        Cycles through the four stages in order, looping after completion.
        """
        if not history:
            return "concrete_experience"
        last_stage = history[0].get("stage", "")
        if last_stage == "concrete_experience":
            return "reflective_observation"
        if last_stage == "reflective_observation":
            return "abstract_conceptualization"
        if last_stage == "abstract_conceptualization":
            return "active_experimentation"
        return "concrete_experience"

    def get_system_prompt(self, stage: str) -> str:
        """
        Return stage-specific system prompt.
        """
        base = "You are an educational guide helping a student reflect on their Sugar activity using the Kolb learning cycle."
        prompts = {
            "concrete_experience": f"{base} Ask them exactly what they did or made in this activity.",
            "reflective_observation": f"{base} Ask them what stood out or what they noticed when looking at their work.",
            "abstract_conceptualization": f"{base} Ask them what ideas or patterns occurred to them while working.",
            "active_experimentation": f"{base} Ask them how they might test these ideas next time they do this."
        }
        return prompts.get(stage, prompts["concrete_experience"])

    def get_user_prompt_template(self, stage: str) -> str:
        """Return user prompt template with activity context placeholders."""
        return "I completed a {duration} '{title}' {activity_type} activity. Can you guide my reflection?"
