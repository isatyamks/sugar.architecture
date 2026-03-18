"""
Adaptive prompt generator.

Assembles the final LLM prompt by combining:
- Framework-specific system prompt
- Framework-specific user prompt template
- Activity context (title, type, duration, history)
- Learner profile (age, language)

Also handles language and complexity adaptation so that the prompt
is appropriate for the learner's level.
"""

from app.core.frameworks.base import BaseReflectionFramework
from app.api.v1.schemas.request import ReflectionRequest


class PromptGenerator:
    """
    Constructs the final prompt payload sent to the LLM provider.
    """

    def build_prompt(
        self,
        framework: BaseReflectionFramework,
        stage: str,
        request: ReflectionRequest,
    ) -> dict:
        """
        Build the complete prompt dict with 'system' and 'user' keys.
        """
        system_prompt = framework.get_system_prompt(stage)
        
        # Format the user prompt template with context values
        user_template = framework.get_user_prompt_template(stage)
        ctx = request.context
        user_prompt = user_template.format(
            title=ctx.title,
            description=ctx.description or "",
            activity_type=ctx.bundle_id.split(".")[-1] if ctx.bundle_id else "activity",
            duration=f"{ctx.duration_seconds // 60} minutes" if ctx.duration_seconds else "a while"
        )
        
        # Adaptation for age
        age = request.learner.age if request.learner else None
        system_prompt = self._adapt_for_age(system_prompt, age)
        
        # Language adaptation
        language = request.learner.language if request.learner else "en"
        system_prompt = self._adapt_for_language(system_prompt, language)
        
        # Collaboration adaptation (Buddies)
        system_prompt = self._adapt_for_collaboration(system_prompt, ctx.buddies)
        
        # Strict structural constraint
        system_prompt += (
            "\n\nSTRICT CONSTRAINT: You are not a chatbot. "
            "You MUST output exactly ONE short question and nothing else. "
            "Do NOT include conversational filler like 'Great job!' or 'Here is a question'."
        )
        
        # Append history context if available
        if request.history:
            history_text = "\n".join([f"- {h.get('prompt')}: {h.get('response')}" for h in request.history[:3]])
            user_prompt += f"\n\nPrevious reflections for context:\n{history_text}"

        return {
            "system": system_prompt.strip(),
            "user": user_prompt.strip()
        }

    def _adapt_for_age(self, prompt: str, age: int | None) -> str:
        """
        Simplify language for younger learners.
        """
        if age is None:
            return prompt
            
        if age < 8:
            return prompt + "\nRemember to use very simple words, short sentences, and speak directly to a young child."
        elif age <= 12:
            return prompt + "\nKeep your language encouraging, clear, and easy to understand for a middle-schooler."
        
        return prompt

    def _adapt_for_language(self, system_prompt: str, language: str) -> str:
        """
        Add language instruction to the system prompt if non-English.
        """
        language_map = {
            "en": "English",
            "es": "Spanish",
            "pt": "Portuguese",
            "fr": "French",
            "hi": "Hindi"
        }
        
        # If it's not English, explicitly request the language.
        if language and language.lower() != "en":
            lang_name = language_map.get(language[:2].lower(), language)
            system_prompt += f"\nIMPORTANT: You must respond entirely in {lang_name}."
            
        return system_prompt

    def _adapt_for_collaboration(self, system_prompt: str, buddies: list[str]) -> str:
        """
        Adjust prompt persona if the activity was shared with other learners.
        """
        if not buddies:
            return system_prompt
            
        buddy_count = len(buddies)
        return (
            system_prompt + 
            f"\nNote: The learner collaborated with {buddy_count} other buddies on this activity. "
            "Ask a question that focuses on this group interaction, such as how they divided the work, "
            "what changed because they worked together, or how it felt to share the project."
        )
