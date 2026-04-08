"""
LLM Integration module for AI-powered code analysis and optimization.

Supports multiple LLM providers:
- OpenAI (GPT-3.5, GPT-4)
- Groq (Free tier available)
"""

import os
from typing import Optional, Dict, Any
from enum import Enum
import json


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    GROQ = "groq"


class LLMConfig:
    """Configuration for LLM integration."""

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.GROQ,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """
        Initialize LLM configuration.

        Args:
            provider: LLM provider to use.
            api_key: API key for the provider.
            model: Model identifier.
            temperature: Temperature for generation (0-1).
            max_tokens: Maximum tokens for response.
        """
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Set defaults and environment variables
        if provider == LLMProvider.OPENAI:
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.model = model or "gpt-3.5-turbo"
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not provided. Set OPENAI_API_KEY environment variable."
                )
        elif provider == LLMProvider.GROQ:
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            self.model = model or "mixtral-8x7b-32768"
            if not self.api_key:
                raise ValueError(
                    "Groq API key not provided. Set GROQ_API_KEY environment variable."
                )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "provider": self.provider.value,
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


class OpenAIModel(BaseLanguageModel):
    """OpenAI GPT model integration."""

    def __init__(self, config: LLMConfig):
        """Initialize OpenAI model."""
        super().__init__(config)
        try:
            import openai
            openai.api_key = config.api_key
            self.client = openai.OpenAI(api_key=config.api_key)
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )

    def generate(self, prompt: str) -> str:
        """
        Generate response using OpenAI API.

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
            raise RuntimeError(f"OpenAI API error: {e}")

    def stream(self, prompt: str):
        """
        Stream response from OpenAI API.

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
            raise RuntimeError(f"OpenAI streaming error: {e}")


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
    Main integrator for LLM services.

    Abstracts the complexity of multiple providers.
    """

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.GROQ,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize LLM integrator.

        Args:
            provider: LLM provider to use.
            api_key: API key for provider.
            model: Model identifier.
        """
        config = LLMConfig(provider=provider, api_key=api_key, model=model)

        if provider == LLMProvider.OPENAI:
            self.model = OpenAIModel(config)
        elif provider == LLMProvider.GROQ:
            self.model = GroqModel(config)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

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
        """Get information about the current LLM provider."""
        return {
            "provider": self.config.provider.value,
            "model": self.config.model,
            "max_tokens": str(self.config.max_tokens),
        }


def create_llm_integrator(provider: str = "groq", **kwargs) -> LLMIntegrator:
    """
    Factory function to create LLM integrator.

    Args:
        provider: Provider name ("openai" or "groq").
        **kwargs: Additional arguments for LLMIntegrator.

    Returns:
        LLMIntegrator: Initialized integrator.
    """
    provider_enum = LLMProvider[provider.upper()]
    return LLMIntegrator(provider=provider_enum, **kwargs)
