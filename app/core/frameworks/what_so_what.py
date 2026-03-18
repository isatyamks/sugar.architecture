"""
What? So What? Now What? framework.

Stages: What → So What → Now What

The most accessible framework. Default for younger learners (< 12).
Uses simple, direct language to guide the learner through three
levels of reflection: describing, interpreting, and planning.
"""

from typing import List
from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ActivityContext


class WhatSoWhatFramework(BaseReflectionFramework):
    """
    Three-stage reflection: What happened, why it matters, what's next.
    """

    STAGES = ["what", "so_what", "now_what"]

    @property
    def name(self) -> str:
        return "What? So What? Now What?"

    @property
    def stages(self) -> List[str]:
        return self.STAGES

    def select_stage(self, context: ActivityContext, history: List[dict]) -> str:
        """
        Select stage based on history.
        Simple three-step rotation.
        """
        if not history:
            return "what"
        last_stage = history[0].get("stage", "")
        if last_stage == "what":
            return "so_what"
        if last_stage == "so_what":
            return "now_what"
        return "what"

    def get_system_prompt(self, stage: str) -> str:
        """
        Return system prompt for each phase.
        """
        base = "You are a friendly learning companion for a child using Sugar learning activities."
        prompts = {
            "what": f"{base} Ask them a simple, single question about what they just made or did.",
            "so_what": f"{base} Ask them a simple question about what part of what they did was interesting, or what they learned from it.",
            "now_what": f"{base} Ask them what they would want to try differently next time.",
        }
        return prompts.get(stage, prompts["what"])

    def get_user_prompt_template(self, stage: str) -> str:
        """Return user prompt template using child-friendly language."""
        return "I just finished a {activity_type} activity called '{title}'. Can you ask me a question about it?"
