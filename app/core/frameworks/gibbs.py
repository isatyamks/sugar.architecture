"""
Gibbs Reflective Cycle implementation.

Stages: Description → Feelings → Evaluation → Analysis → Conclusion → Action Plan

Suitable for older learners (12+) with more structured reflective capacity.
This is the most detailed framework, guiding the learner through a
comprehensive six-stage cycle from describing the experience to
creating an action plan for future improvement.
"""

from typing import List
from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ActivityContext


class GibbsFramework(BaseReflectionFramework):
    """
    Gibbs reflective cycle: 6 stages from description to action planning.
    """

    STAGES = [
        "description",
        "feelings",
        "evaluation",
        "analysis",
        "conclusion",
        "action_plan",
    ]

    @property
    def name(self) -> str:
        return "Gibbs Reflective Cycle"

    @property
    def stages(self) -> List[str]:
        return self.STAGES

    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Select stage based on how many prior reflections exist in history.
        Cycles through stages sequentially. If the learner has completed
        all 6, loops back to 'description' for deeper reflection.
        """
        if not history:
            return "description"
            
        stages_order = self.STAGES
        last_stage = history[0].get("stage", "")
        
        try:
            idx = stages_order.index(last_stage)
            next_idx = (idx + 1) % len(stages_order)
            return stages_order[next_idx]
        except ValueError:
            return "description"

    def get_system_prompt(self, stage: str) -> str:
        """
        Return the system prompt for the Gibbs stage.
        """
        base = "You are a mature learning guide leading an older student through a Gibbs Reflective Cycle."
        prompts = {
            "description": f"{base} Ask them to describe factually what happened during their activity.",
            "feelings": f"{base} Ask them what they were feeling or thinking while they were working.",
            "evaluation": f"{base} Ask them to evaluate what went well or what went badly in this activity.",
            "analysis": f"{base} Ask them to analyze and make sense of the situation, finding reasons why it happened that way.",
            "conclusion": f"{base} Ask what else could have been done and what they ultimately learned.",
            "action_plan": f"{base} Ask them to outline an action plan for what they will do differently next time."
        }
        return prompts.get(stage, prompts["description"])

    def get_user_prompt_template(self, stage: str) -> str:
        """
        Return a user prompt template with {title}, {description},
        {activity_type}, {duration} placeholders.
        """
        return "I completed a {activity_type} activity named '{title}' that took {duration}. Please guide me through the next step of reflection."
