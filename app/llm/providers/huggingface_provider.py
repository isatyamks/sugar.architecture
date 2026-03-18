"""
HuggingFace Inference API provider.

Uses the HuggingFace serverless Inference API or dedicated Inference Endpoints
for model inference without hosting infrastructure.

Ref: https://huggingface.co/docs/api-inference/
"""

from app.llm.base_provider import BaseLLMProvider


class HuggingFaceProvider(BaseLLMProvider):
    """
    HuggingFace Inference API provider.
    """

    def __init__(self, api_key: str, model_id: str = "meta-llama/Llama-3-8B-Instruct"):
        """
        Args:
            api_key: HuggingFace API token.
            model_id: Model repository ID on HuggingFace Hub.
        """
        self._api_key = api_key
        self._model_id = model_id

    @property
    def provider_name(self) -> str:
        return "huggingface"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """
        Call the HuggingFace Inference API.

        Implementation should:
        1. POST to https://api-inference.huggingface.co/models/{model_id}
        2. Include Authorization header
        3. Format input as text-generation or conversational payload
        4. Return the generated text
        """
        ...

    async def health_check(self) -> bool:
        """Check if the model is loaded on HuggingFace infrastructure."""
        ...
