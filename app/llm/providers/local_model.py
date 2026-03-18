"""
Local model provider.

Loads a model from disk using HuggingFace transformers or PEFT.
Intended for self-hosted deployments on school servers or personal machines.
"""

import asyncio
import json
import logging
from pathlib import Path

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    HAS_LOCAL_DEPS = True
except ImportError:
    HAS_LOCAL_DEPS = False

from app.llm.base_provider import BaseLLMProvider
from app.exceptions.handlers import LLMProviderError


logger = logging.getLogger(__name__)


class LocalModelProvider(BaseLLMProvider):
    """
    Self-hosted LLM inference using a local model checkpoint.
    """

    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Args:
            model_path: Path to the model weights directory or GGUF file.
            device: Inference device — "cpu" | "cuda" | "auto".
        """
        self._model_path = model_path
        self._device = device
        self._model = None
        self._tokenizer = None
        self._loaded = False
        
        if not HAS_LOCAL_DEPS:
            logger.warning("LocalModelProvider requires transformers, torch, and peft. Please install optional dependencies.")

    @property
    def provider_name(self) -> str:
        return "local"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """
        Run inference on the locally loaded model.
        """
        if not HAS_LOCAL_DEPS:
            raise LLMProviderError(self.provider_name, "Missing dependencies (transformers, torch, peft).")

        # 1. Lazy-load model on first call
        if not self._loaded:
            self._load_model()
            
        # 2. Format prompts using the model's chat template
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        try:
            if hasattr(self._tokenizer, "apply_chat_template"):
                input_text = self._tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
            else:
                input_text = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"

            inputs = self._tokenizer(input_text, return_tensors="pt").to(self._model.device)

            # 3. Run generation in a separate thread to avoid blocking FastAPI event loop
            def _run_inference():
                with torch.no_grad():
                    outputs = self._model.generate(
                        **inputs,
                        max_new_tokens=max_tokens,
                        temperature=temperature,
                        top_p=0.9,
                        do_sample=True,
                        pad_token_id=self._tokenizer.pad_token_id,
                    )
                new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
                return self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

            response_text = await asyncio.to_thread(_run_inference)
            return response_text
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise LLMProviderError(self.provider_name, f"Inference error: {str(e)}")

    async def health_check(self) -> bool:
        """Return True if the model is loaded and can generate."""
        if not HAS_LOCAL_DEPS:
            return False
            
        if not self._loaded:
            try:
                # Basic check if path exists if model isn't warm yet
                return Path(self._model_path).exists()
            except Exception:
                return False
        return True

    def _load_model(self) -> None:
        """
        Lazy-load the model and tokenizer into memory.
        Called once on first generate() invocation.
        """
        logger.info(f"Loading local model from {self._model_path}...")
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self._model_path)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token

            config_path = Path(self._model_path) / "adapter_config.json"
            if config_path.exists():
                logger.info("Adapter config detected. Loading PEFT model...")
                with open(config_path) as f:
                    adapter_cfg = json.load(f)
                base_model = adapter_cfg.get("base_model_name_or_path", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
                
                base = AutoModelForCausalLM.from_pretrained(
                    base_model,
                    dtype=torch.float32,
                    device_map=self._device,
                )
                self._model = PeftModel.from_pretrained(base, self._model_path)
            else:
                logger.info("Loading standard causal LM...")
                self._model = AutoModelForCausalLM.from_pretrained(
                    self._model_path,
                    dtype=torch.float32,
                    device_map=self._device,
                )
            
            self._model.eval()
            self._loaded = True
            logger.info("Local model successfully loaded.")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise LLMProviderError(self.provider_name, f"Load error: {str(e)}")
