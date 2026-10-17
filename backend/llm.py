"""Provider-agnostic LLM calls: prompt builders and OpenAI-format SSE streaming.

Both supported providers (OpenRouter, Ollama) speak the OpenAI chat completions
protocol, so one streaming implementation serves them; a
:class:`backend.chat_config.ChatSettings` carries the resolved URL and key.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from backend.chat_config import ChatSettings

TUTOR_SYSTEM_PROMPT = (
    "You are a data engineering tutor. Expand the notebook section the student "
    "is reading: teach the concept with one worked example and the common pitfalls."
)

CHAT_SYSTEM_PROMPT = "You are a data engineering tutor helping a student with their notebook."


def make_client() -> httpx.AsyncClient:
    """Build the HTTP client used for provider calls (monkeypatched in tests)."""
    return httpx.AsyncClient(timeout=60.0)


def elaborate_messages(section_markdown: str, context_cells: list[str]) -> list[dict[str, str]]:
    """Fixed system prompt + the section markdown with its surrounding cells.

    ``context_cells`` is already sliced by the frontend (up to 3 on each side).
    """
    parts = [f"### Notebook section\n\n{section_markdown}"]
    if context_cells:
        rendered = "\n\n".join(
            f"Cell {i + 1}:\n```\n{cell}\n```" for i, cell in enumerate(context_cells)
        )
        parts.append(f"### Surrounding cells\n\n{rendered}")
    return [
        {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
        {"role": "user", "content": "\n\n".join(parts)},
    ]


def chat_messages(
    notebook_title: str,
    outline: list[str],
    visible_section: str,
    history: list[dict[str, str]],
    message: str,
) -> list[dict[str, str]]:
    """Notebook-context system prompt, then the chat history, then the question."""
    outline_bullets = "\n".join(f"- {item}" for item in outline)
    system_content = (
        f"{CHAT_SYSTEM_PROMPT}\n\n"
        f"The student is reading the notebook '{notebook_title}'.\n\n"
        f"Notebook outline:\n{outline_bullets}\n\n"
        f"The section currently on screen:\n\n{visible_section}"
    )
    return [
        {"role": "system", "content": system_content},
        *history,
        {"role": "user", "content": message},
    ]


async def stream_llm(
    settings: ChatSettings, messages: list[dict[str, str]]
) -> AsyncIterator[dict[str, object]]:
    """Stream a chat completion as ``{"delta": str}`` events.

    Never raises: a non-200 status, a network failure, or a malformed stream
    yields one ``{"error": str}`` event naming the provider, then the stream
    ends.
    """
    payload = {
        "model": settings.model,
        "messages": messages,
        "stream": True,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
    }
    headers = {"Authorization": f"Bearer {settings.api_key}"}
    try:
        async with make_client() as client:
            async with client.stream(
                "POST", settings.base_url, headers=headers, json=payload
            ) as response:
                if response.status_code != 200:
                    yield {"error": await _status_error(settings.provider, response)}
                    return
                async for chunk in _chunks(response.aiter_lines(), settings.provider):
                    yield chunk
    except httpx.HTTPError as exc:
        yield {"error": f"{settings.provider} request failed: {exc}"}


async def _chunks(lines: AsyncIterator[str], provider: str) -> AsyncIterator[dict[str, str]]:
    """Parse provider SSE (``data: {json}``, ``[DONE]`` sentinel) into deltas."""
    async for line in lines:
        if not line.startswith("data:"):
            continue
        payload = line[len("data:") :].strip()
        if payload == "[DONE]":
            return
        try:
            content = json.loads(payload)["choices"][0].get("delta", {}).get("content")
        except (json.JSONDecodeError, KeyError, IndexError, TypeError, AttributeError):
            yield {"error": f"{provider} returned a malformed streaming chunk"}
            return
        if content:
            yield {"delta": content}


async def _status_error(provider: str, response: httpx.Response) -> str:
    body = (await response.aread()).decode(errors="replace")
    return f"{provider} request failed with HTTP {response.status_code}: {body.strip()[:200]}"
