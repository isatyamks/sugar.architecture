"""
KWL (Know / Want / Learned) framework.

Stages: Know → Want → Learned

Suitable for reading and writing activities (e.g. Write, Browse, Wikipedia).
Guides the learner to reflect on what they knew before, what they wanted to find out,
and what they actually learned.
"""

from typing import List
from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ActivityContext

class KWLFramework(BaseReflectionFramework):
    """
    KWL reflective cycle.
    """

    STAGES = ["know", "want", "learned"]

    @property
    def name(self) -> str:
        return "KWL (Know/Want/Learned)"

    @property
    def stages(self) -> List[str]:
        return self.STAGES

    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Select stage based on history.
        Simple three-step rotation for KWL.
        """
        if not history:
            return "know"
        last_stage = history[0].get("stage", "")
        if last_stage == "know":
            return "want"
        if last_stage == "want":
            return "learned"
        return "know"

    def get_system_prompt(self, stage: str) -> str:
        """Return system prompt for each phase."""
        base = "You are an educational guide helping a student reflect on a reading or writing activity."
        prompts = {
            "know": f"{base} Ask them what they already knew about this topic before they started.",
            "want": f"{base} Ask them what they wanted to find out or what questions they had.",
            "learned": f"{base} Ask them what new thing they actually learned or discovered.",
        }
        return prompts.get(stage, prompts["know"])

    def get_user_prompt_template(self, stage: str) -> str:
        """Return user prompt template using child-friendly language."""
        return "I was working on a '{title}' {activity_type} activity. Can you guide my reflection?"
