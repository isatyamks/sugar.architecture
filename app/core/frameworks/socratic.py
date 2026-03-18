"""
Socratic Questioning framework.

Stages: Clarification → Probing Assumptions → Probing Reasons → Viewpoints → Implications

Suitable for coding, procedural, and problem-solving activities (e.g. Turtle, Pippy, Calculate).
Focuses on "why" the learner made specific choices and what the alternatives are.
"""

from typing import List
from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ActivityContext


class SocraticFramework(BaseReflectionFramework):
    """
    Socratic questioning reflection framework.
    """

    STAGES = [
        "clarification",
        "probing_assumptions",
        "probing_reasons",
        "viewpoints",
        "implications"
    ]

    @property
    def name(self) -> str:
        return "Socratic Questioning"

    @property
    def stages(self) -> List[str]:
        return self.STAGES

    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Select stage based on history depth.
        """
        if not history:
            return "clarification"
        
        stages_order = self.STAGES
        last_stage = history[0].get("stage", "")
        
        try:
            idx = stages_order.index(last_stage)
            next_idx = (idx + 1) % len(stages_order)
            return stages_order[next_idx]
        except ValueError:
            return "clarification"

    def get_system_prompt(self, stage: str) -> str:
        """Return system prompt for each phase."""
        base = "You are a Socratic tutor guiding a student who just finished a coding or problem-solving activity."
        prompts = {
            "clarification": f"{base} Ask them to clarify exactly what goal they were trying to achieve.",
            "probing_assumptions": f"{base} Ask them what they assumed would happen when they tried their approach.",
            "probing_reasons": f"{base} Ask them *why* they chose the specific method or logic they used.",
            "viewpoints": f"{base} Ask them if there was another completely different way they could have solved it.",
            "implications": f"{base} Ask them how they could use this same logic in a different problem.",
        }
        return prompts.get(stage, prompts["clarification"])

    def get_user_prompt_template(self, stage: str) -> str:
        """Return user prompt template using child-friendly language."""
        return "I completed a the '{title}' {activity_type}. Please ask me a question to help me think deeper about it."
