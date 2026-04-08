"""
LLM Integration module for AI-powered code analysis and optimization.

Uses Groq as the LLM provider (free tier available).
"""

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
        """
        Initialize Groq LLM configuration.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var).
            model: Model identifier (defaults to mixtral-8x7b-32768).
            temperature: Temperature for generation (0-1).
            max_tokens: Maximum tokens for response.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or "mixtral-8x7b-32768"
        self.temperature = temperature
        self.max_tokens = max_tokens

        if not self.api_key:
            raise ValueError(
                "Groq API key not provided. Set GROQ_API_KEY environment variable."
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "provider": "groq",
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


class BaseLanguageModel:
    """Base class for language model implementations."""

    def __init__(self, config: LLMConfig):
        """Initialize base model."""
        self.config = config

    def generate(self, prompt: str) -> str:
        """
        Generate response from prompt.

        Args:
            prompt: Input prompt.

        Returns:
            str: Generated response.
        """
        raise NotImplementedError

    def stream(self, prompt: str):
        """
        Stream response from prompt.

        Args:
            prompt: Input prompt.

        Yields:
            str: Response chunks.
        """
        raise NotImplementedError




class GroqModel(BaseLanguageModel):
    """Groq language model integration."""

    def __init__(self, config: LLMConfig):
        """Initialize Groq model."""
        super().__init__(config)
        try:
            from groq import Groq
            self.client = Groq(api_key=config.api_key)
        except ImportError:
            raise ImportError(
                "Groq package not installed. Install with: pip install groq"
            )

    def generate(self, prompt: str) -> str:
        """
        Generate response using Groq API.

        Args:
            prompt: Input prompt.

        Returns:
            str: Generated response.
        """
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
        """
        Stream response from Groq API.

        Args:
            prompt: Input prompt.

        Yields:
            str: Response chunks.
        """
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
    """
    Main integrator for Groq LLM services.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize Groq LLM integrator.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var).
            model: Model identifier (defaults to mixtral-8x7b-32768).
        """
        config = LLMConfig(api_key=api_key, model=model)
        self.model = GroqModel(config)
        self.config = config

    def generate(self, prompt: str, stream: bool = False):
        """
        Generate response from prompt.

        Args:
            prompt: Input prompt.
            stream: Whether to stream response.

        Returns:
            str: Generated response (or generator if streaming).
        """
        if stream:
            return self.model.stream(prompt)
        else:
            return self.model.generate(prompt)

    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current Groq provider."""
        return {
            "provider": "groq",
            "model": self.config.model,
            "max_tokens": str(self.config.max_tokens),
        }


def create_llm_integrator(**kwargs) -> LLMIntegrator:
    """
    Factory function to create Groq LLM integrator.

    Args:
        **kwargs: Additional arguments for LLMIntegrator (api_key, model).

    Returns:
        LLMIntegrator: Initialized Groq integrator.
    """
    return LLMIntegrator(**kwargs)
