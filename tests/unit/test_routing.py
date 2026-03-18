"""
Unit tests for FrameworkRouter.
"""

import pytest
from app.core.routing import FrameworkRouter
from app.api.v1.schemas.common import ReflectionFramework


class TestFrameworkRouter:
    """Tests for the framework routing logic."""

    def test_explicit_override_takes_priority(self):
        """When framework_override is set, that framework should be returned."""
        ...

    def test_young_learner_gets_what_so_what(self):
        """Age < min_age_for_gibbs should route to What-So-What."""
        ...

    def test_older_learner_gets_gibbs(self):
        """Age >= min_age_for_gibbs should route to Gibbs."""
        ...

    def test_unknown_age_uses_default(self):
        """When age is None, should use the config default framework."""
        ...

    def test_unregistered_framework_raises(self):
        """Requesting an unregistered framework should raise FrameworkNotFoundError."""
        ...
