"""
Framework routing logic.

Determines which reflective practice framework to use based on:
- Learner age (younger → simpler frameworks)
- Activity bundle_id (creative vs analytical activities)
- Explicit override from the request
- Configuration defaults
"""

from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ReflectionRequest
from app.api.v1.schemas.common import ReflectionFramework
from app.config import get_settings


class FrameworkRouter:
    """
    Route a reflection request to the appropriate framework instance.
    """

    def __init__(
        self, frameworks: dict[ReflectionFramework, BaseReflectionFramework]
    ):
        """
        Args:
            frameworks: Map of framework enum → framework instance.
                        All registered frameworks available for routing.
        """
        self._frameworks = frameworks

    def route(self, request: ReflectionRequest) -> BaseReflectionFramework:
        """
        Select framework for this request.
        """
        settings = get_settings()

        # 1. Explicit override
        if request.framework_override and request.framework_override in self._frameworks:
            return self._frameworks[request.framework_override]

        # 2. Activity-type heuristics (Highest priority after explicit override)
        activity_fw = self._route_by_activity(request.context.bundle_id)
        if activity_fw and activity_fw in self._frameworks:
            return self._frameworks[activity_fw]

        # 3. Age-based routing (Fallback if activity type is not recognized)
        age = request.learner.age if request.learner else None
        age_fw = self._route_by_age(age, settings)
        if age_fw and age_fw in self._frameworks:
            return self._frameworks[age_fw]

        # 4. Config default
        default_fw_value = ReflectionFramework(settings.default_framework)
        if default_fw_value in self._frameworks:
            return self._frameworks[default_fw_value]

        # Fallback to whatever is available
        from app.exceptions.handlers import FrameworkNotFoundError
        if not self._frameworks:
            raise FrameworkNotFoundError("No frameworks registered")
        return next(iter(self._frameworks.values()))

    def _route_by_age(self, age: int | None, settings) -> ReflectionFramework | None:
        """
        Return a framework enum based on learner age.
        """
        if age is None:
            return None
        if age < settings.min_age_for_gibbs:
            return ReflectionFramework.WHAT_SO_WHAT
        return ReflectionFramework.GIBBS

    def _route_by_activity(self, bundle_id: str) -> ReflectionFramework | None:
        """
        Return a framework enum based on activity type heuristics.
        """
        bundle_lower = bundle_id.lower()
        
        # Knowledge / Reading / Writing activities map to KWL
        knowledge_keywords = ["write", "read", "browse", "wikipedia"]
        if any(keyword in bundle_lower for keyword in knowledge_keywords):
            return ReflectionFramework.KWL
            
        # Procedural / Coding activities map to Socratic
        procedural_keywords = ["turtle", "pippy", "calculate", "music"]
        if any(keyword in bundle_lower for keyword in procedural_keywords):
            return ReflectionFramework.SOCRATIC
            
        # Expressive / Art activities map to Kolb
        creative_keywords = ["paint", "sketch", "draw", "record"]
        if any(keyword in bundle_lower for keyword in creative_keywords):
            return ReflectionFramework.KOLB
            
        return None
