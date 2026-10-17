"""Tests for chat config loading and the /chat SSE endpoints.

The provider HTTP layer is faked with ``httpx.MockTransport`` behind
``llm.make_client`` — the same seam it is designed for — so the endpoint
tests exercise the real provider call path: URL, auth header, SSE parsing.
"""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import llm, main
from backend.chat_config import (
    PROVIDER_BASE_URLS,
    MissingKeyError,
    load_chat_settings,
)

OLLAMA_CONFIG = """\
provider: ollama
model: gpt-oss-large
max_tokens: 512
temperature: 0.3
"""

Handler = Callable[[httpx.Request], httpx.Response]


@pytest.fixture(autouse=True)
def clean_chat_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep developer-machine chat credentials out of the test results."""
    for var in ("OPENROUTER_API_KEY", "OLLAMA_API_KEY", "CHAT_PROVIDER", "CHAT_MODEL"):
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def client() -> TestClient:
    return TestClient(main.app)


@pytest.fixture
def fake_provider(monkeypatch: pytest.MonkeyPatch) -> Callable[[Handler], list[httpx.Request]]:
    """Route provider calls through a MockTransport handler.

    Returns an installer; calling it wires ``llm.make_client`` to the fake
    and hands back the requests the code made, for call-shape assertions.
    """

    def install(handler: Handler) -> list[httpx.Request]:
        seen: list[httpx.Request] = []

        def recording_handler(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            return handler(request)

        transport = httpx.MockTransport(recording_handler)
        monkeypatch.setattr(llm, "make_client", lambda: httpx.AsyncClient(transport=transport))
        return seen

    return install


def _sse_body(chunks: list[str]) -> bytes:
    events = [
        f"data: {json.dumps({'choices': [{'delta': {'content': chunk}}]})}\n\n"
        for chunk in chunks
    ]
    events.append("data: [DONE]\n\n")
    return "".join(events).encode()


def _parse_sse_events(raw: str) -> list[dict[str, Any]]:
    return [
        json.loads(event.removeprefix("data: "))
        for event in raw.split("\n\n")
        if event.startswith("data: ")
    ]


def _chat_body(mode: str, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "mode": mode,
        "section_markdown": "# Section\nBody text",
        "context_cells": ["x = 1", "print(x)"],
        "notebook_title": "Spark fundamentals",
        "outline": ["Intro", "Partitions"],
        "visible_section": "# Section",
        "history": [{"role": "user", "content": "earlier question"}],
        "message": "what is a partition?",
    }
    body.update(overrides)
    return body


class TestLoadChatSettings:
    def test_config_file_resolves_provider_base_url(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("OLLAMA_API_KEY", "ollama-key")
        (tmp_path / "chat.config.yml").write_text(OLLAMA_CONFIG)

        settings = load_chat_settings(tmp_path)

        assert settings.provider == "ollama"
        assert settings.model == "gpt-oss-large"
        assert settings.base_url == PROVIDER_BASE_URLS["ollama"]
        assert settings.api_key == "ollama-key"
        assert settings.max_tokens == 512
        assert settings.temperature == pytest.approx(0.3)

    def test_env_overrides_beat_config_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "key")
        (tmp_path / "chat.config.yml").write_text(OLLAMA_CONFIG)
        monkeypatch.setenv("CHAT_PROVIDER", "openrouter")
        monkeypatch.setenv("CHAT_MODEL", "custom/model")

        settings = load_chat_settings(tmp_path)

        assert settings.provider == "openrouter"
        assert settings.model == "custom/model"
        assert settings.base_url == PROVIDER_BASE_URLS["openrouter"]

    def test_missing_config_file_uses_example_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "key")

        settings = load_chat_settings(tmp_path)

        assert settings.provider == "openrouter"
        assert settings.model == "anthropic/claude-sonnet-4.5"

    def test_missing_key_raises_with_env_var_name(self, tmp_path: Path) -> None:
        with pytest.raises(MissingKeyError) as exc_info:
            load_chat_settings(tmp_path)

        assert exc_info.value.env_var == "OPENROUTER_API_KEY"
        assert "OPENROUTER_API_KEY" in str(exc_info.value)

    def test_missing_ollama_key_names_ollama_env_var(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        (tmp_path / "chat.config.yml").write_text(OLLAMA_CONFIG)

        with pytest.raises(MissingKeyError) as exc_info:
            load_chat_settings(tmp_path)

        assert exc_info.value.env_var == "OLLAMA_API_KEY"


class TestPromptBuilders:
    def test_elaborate_messages_use_fixed_system_prompt_and_context(self) -> None:
        messages = llm.elaborate_messages("# Section\nBody", ["x = 1", "print(x)"])

        assert messages[0] == {
            "role": "system",
            "content": (
                "You are a data engineering tutor. Expand the notebook section the "
                "student is reading: teach the concept with one worked example and "
                "the common pitfalls."
            ),
        }
        assert messages[1]["role"] == "user"
        user_content = messages[1]["content"]
        assert "# Section\nBody" in user_content
        assert "x = 1" in user_content
        assert "print(x)" in user_content

    def test_chat_messages_keep_history_and_notebook_context(self) -> None:
        history = [{"role": "user", "content": "earlier question"}]

        messages = llm.chat_messages(
            notebook_title="Spark fundamentals",
            outline=["Intro", "Partitions"],
            visible_section="# Partitions",
            history=history,
            message="what is a partition?",
        )

        assert [m["role"] for m in messages] == ["system", "user", "user"]
        assert "Spark fundamentals" in messages[0]["content"]
        assert "- Intro" in messages[0]["content"]
        assert "- Partitions" in messages[0]["content"]
        assert "# Partitions" in messages[0]["content"]
        assert messages[1] == history[0]
        assert messages[-1]["content"] == "what is a partition?"


class TestChatEndpoint:
    def test_streaming_assembles_deltas_until_done(
        self,
        client: TestClient,
        fake_provider: Callable[[Handler], list[httpx.Request]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        seen = fake_provider(
            lambda request: httpx.Response(200, content=_sse_body(["Hello ", "world"]))
        )

        response = client.post("/chat", json=_chat_body("elaborate"))

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        events = _parse_sse_events(response.text)
        text = "".join(event["delta"] for event in events if "delta" in event)
        assert text == "Hello world"
        assert events[-1] == {"done": True}

        request = seen[0]
        assert str(request.url) == PROVIDER_BASE_URLS["openrouter"]
        assert request.headers["Authorization"] == "Bearer test-key"
        payload = json.loads(request.content)
        assert payload["model"] == "anthropic/claude-sonnet-4.5"
        assert payload["stream"] is True
        assert payload["messages"][0]["role"] == "system"
        assert payload["max_tokens"] == 1024
        assert payload["temperature"] == pytest.approx(0.7)

    def test_chat_mode_sends_history_and_message(
        self,
        client: TestClient,
        fake_provider: Callable[[Handler], list[httpx.Request]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        seen = fake_provider(lambda request: httpx.Response(200, content=_sse_body(["ok"])))

        client.post("/chat", json=_chat_body("chat"))

        payload = json.loads(seen[0].content)
        roles = [m["role"] for m in payload["messages"]]
        assert roles == ["system", "user", "user"]
        assert payload["messages"][-1]["content"] == "what is a partition?"
        assert "earlier question" in payload["messages"][1]["content"]

    def test_provider_500_yields_error_event_mentioning_provider(
        self,
        client: TestClient,
        fake_provider: Callable[[Handler], list[httpx.Request]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        fake_provider(lambda request: httpx.Response(500, text="server exploded"))

        response = client.post("/chat", json=_chat_body("elaborate"))

        events = _parse_sse_events(response.text)
        assert any(
            "error" in event and "openrouter" in event["error"] for event in events
        )
        assert "server exploded" in response.text
        assert all("delta" not in event for event in events)

    def test_missing_key_returns_400_naming_env_var(
        self, client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(main, "ROOT", tmp_path)

        response = client.post("/chat", json=_chat_body("elaborate"))

        assert response.status_code == 400
        assert "OPENROUTER_API_KEY" in response.json()["detail"]

    def test_invalid_mode_rejected(self, client: TestClient) -> None:
        response = client.post("/chat", json=_chat_body("explain"))

        assert response.status_code == 400


class TestChatSettingsEndpoint:
    def test_key_absent_reports_false(self, client: TestClient) -> None:
        response = client.get("/chat/settings")

        body = response.json()
        assert response.status_code == 200
        assert body["provider"] == "openrouter"
        assert body["model"] == "anthropic/claude-sonnet-4.5"
        assert body["key_present"] is False
        assert "api_key" not in body

    def test_key_present_reports_true(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "secret")

        body = client.get("/chat/settings").json()

        assert body["key_present"] is True
        assert "api_key" not in body