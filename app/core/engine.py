"""
Reflection engine — central orchestrator.

Orchestrates the end-to-end flow:
  request → framework routing → prompt construction → LLM inference → response

This class is stateless and composed via dependency injection.
"""

from app.core.routing import FrameworkRouter
from app.core.prompt_generator import PromptGenerator
from app.llm.fallback import FallbackManager
from app.api.v1.schemas.request import ReflectionRequest
from app.api.v1.schemas.response import ReflectionPrompt


class ReflectionEngine:
    """
    Stateless orchestrator for reflection prompt generation.

    Composes: FrameworkRouter → PromptGenerator → FallbackManager(LLM)
    """

    def __init__(
        self,
        router: FrameworkRouter,
        prompt_generator: PromptGenerator,
        llm_manager: FallbackManager,
    ):
        """
        Args:
            router: Selects the reflection framework based on request context.
            prompt_generator: Builds the final LLM prompt from framework + context.
            llm_manager: Manages LLM inference with fallback chain.
        """
        self._router = router
        self._prompt_generator = prompt_generator
        self._llm_manager = llm_manager

    async def generate(self, request: ReflectionRequest) -> ReflectionPrompt:
        """
        Execute the full reflection pipeline.
        """
        # 1. Select framework via router
        framework = self._router.route(request)
        
        # 2. Determine the current reflection stage
        stage = framework.select_stage(
            context=request.context, 
            history=request.history or []
        )
        
        # 3. Build the LLM prompt via prompt_generator
        prompt_dicts = self._prompt_generator.build_prompt(
            framework=framework,
            stage=stage,
            request=request
        )
        
        # 4. Call LLM via fallback_manager
        response_text, provider_name = await self._llm_manager.generate(
            system_prompt=prompt_dicts["system"],
            user_prompt=prompt_dicts["user"]
        )
        
        # 5. Parse and return structured ReflectionPrompt
        framework_enum = next((k for k, v in self._router._frameworks.items() if v == framework), None)
        
        return ReflectionPrompt(
            prompt_text=response_text,
            framework_used=framework_enum,
            stage=stage,
            model_version=provider_name
        )
