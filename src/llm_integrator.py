"""LLM Integration module for AI-powered code analysis using Groq."""

import os
from typing import Optional, Dict, Any
import json


class LLMConfig:
    """Configuration for Groq LLM integration."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or "mixtral-8x7b-32768"
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError(
                "Groq API key not provided. Set GROQ_API_KEY environment variable."
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": "groq",
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


class BaseLanguageModel:
    """Base class for language model implementations."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    def stream(self, prompt: str):
        raise NotImplementedError




class GroqModel(BaseLanguageModel):
    """Groq language model integration."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from groq import Groq
            self.client = Groq(api_key=config.api_key)
        except ImportError:
            raise ImportError(
                "Groq package not installed. Install with: pip install groq"
            )

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq API error: {e}")

    def stream(self, prompt: str):
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True,
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise RuntimeError(f"Groq streaming error: {e}")


class LLMIntegrator:
    """Main integrator for Groq LLM services."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        config = LLMConfig(api_key=api_key, model=model)
        self.model = GroqModel(config)
        self.config = config

    def generate(self, prompt: str, stream: bool = False):
        if stream:
            return self.model.stream(prompt)
        else:
            return self.model.generate(prompt)

    def get_provider_info(self) -> Dict[str, str]:
        return {
            "provider": "groq",
            "model": self.config.model,
            "max_tokens": str(self.config.max_tokens),
        }


def create_llm_integrator(**kwargs) -> LLMIntegrator:
    return LLMIntegrator(**kwargs)
