"""Chat provider configuration: ``chat.config.yml`` plus environment overrides.

Provider and model come from ``chat.config.yml`` at the repository root (or
the defaults in ``chat.config.example.yml``); ``CHAT_PROVIDER`` and
``CHAT_MODEL`` override them. API keys never live in the config file — they
come from the environment (``OPENROUTER_API_KEY`` / ``OLLAMA_API_KEY``).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

PROVIDER_BASE_URLS: dict[str, str] = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "ollama": "https://ollama.com/v1/chat/completions",
}

PROVIDER_ENV_KEYS: dict[str, str] = {
    "openrouter": "OPENROUTER_API_KEY",
    "ollama": "OLLAMA_API_KEY",
}

DEFAULT_PROVIDER = "openrouter"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TEMPERATURE = 0.7


class MissingKeyError(Exception):
    """No API key for the configured provider; ``env_var`` names the missing one."""

    def __init__(self, env_var: str) -> None:
        self.env_var = env_var
        super().__init__(
            f"No {env_var} API key is set; export it in the environment to use chat"
        )


class ChatSettings(BaseModel):
    provider: str
    model: str
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    api_key: str
    base_url: str


def load_chat_settings(root: Path) -> ChatSettings:
    """Resolve chat settings from file, env overrides, and the provider's key.

    Raises ``MissingKeyError`` when the provider's API key is absent.
    """
    file_values = _read_config(root)
    provider, model = _resolve_provider_and_model(file_values)
    api_key = os.environ.get(PROVIDER_ENV_KEYS[provider], "")
    if not api_key:
        raise MissingKeyError(PROVIDER_ENV_KEYS[provider])
    return ChatSettings(
        provider=provider,
        model=model,
        max_tokens=file_values.get("max_tokens", DEFAULT_MAX_TOKENS),
        temperature=file_values.get("temperature", DEFAULT_TEMPERATURE),
        api_key=api_key,
        base_url=PROVIDER_BASE_URLS[provider],
    )


def settings_summary(root: Path) -> dict[str, Any]:
    """Endpoint view of the settings: no secrets, no exception when the key is missing."""
    file_values = _read_config(root)
    provider, model = _resolve_provider_and_model(file_values)
    env_var = PROVIDER_ENV_KEYS.get(provider)
    return {
        "provider": provider,
        "model": model,
        "key_present": bool(env_var) and bool(os.environ.get(env_var, "")),
    }


def _resolve_provider_and_model(file_values: dict[str, Any]) -> tuple[str, str]:
    provider = os.environ.get("CHAT_PROVIDER", file_values.get("provider", DEFAULT_PROVIDER))
    model = os.environ.get("CHAT_MODEL", file_values.get("model", DEFAULT_MODEL))
    if provider not in PROVIDER_BASE_URLS:
        raise ValueError(
            f"unknown chat provider {provider!r}; expected one of {sorted(PROVIDER_BASE_URLS)}"
        )
    return provider, model


def _read_config(root: Path) -> dict[str, Any]:
    path = root / "chat.config.yml"
    if not path.is_file():
        return {}
    values = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(values, dict):
        raise ValueError(f"{path} must contain a mapping of chat settings")
    return values