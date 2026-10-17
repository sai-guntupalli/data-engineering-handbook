"""Local interactive viewer backend.

``POST /execute`` runs a notebook cell (or ad-hoc code) in a per-notebook
kernel session; ``POST /reset`` wipes a session's namespace; ``GET /health``
is the liveness probe. ``POST /chat`` streams tutor elaborations/answers from
an LLM provider; ``GET /chat/settings`` reports the chat configuration.
Execution results travel in the body with status 200; only request-shape
problems use HTTP error codes.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, model_validator

from backend import chat_config, sessions
from backend.chat_config import MissingKeyError
from backend.kernel import ExecResult
from backend.llm import chat_messages, elaborate_messages, stream_llm

# Repository root: where chat.config.yml (and its example) live.
ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="Interactive notebook viewer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(RequestValidationError)
async def request_validation_as_400(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Bad request bodies are 400s here, like every other request-shape problem."""
    return JSONResponse({"detail": "invalid request body"}, status_code=400)


@app.exception_handler(MissingKeyError)
async def missing_key_as_400(request: Request, exc: MissingKeyError) -> JSONResponse:
    """A chat request without the provider's API key is a configuration problem."""
    return JSONResponse({"detail": str(exc)}, status_code=400)

# Kernel statuses map onto the HTTP-layer vocabulary: an interrupt-based
# timeout is communicated as "timeout", a dead child as "crashed", and the
# traceback always says what happened.
_HTTP_STATUS = {"ok": "ok", "error": "error", "crashed": "crashed", "interrupted": "timeout"}


class ExecuteRequest(BaseModel):
    notebook: str
    path: str
    cell_index: int | None = None
    code: str | None = None

    @model_validator(mode="after")
    def exactly_one_target(self) -> "ExecuteRequest":
        if (self.cell_index is not None) == (self.code is not None):
            raise ValueError("provide exactly one of cell_index or code")
        return self


class ResetRequest(BaseModel):
    notebook: str


class ChatRequest(BaseModel):
    """One chat request; both modes share the body, each uses its own subset."""

    mode: Literal["elaborate", "chat"]
    section_markdown: str = ""
    context_cells: list[str] = Field(default_factory=list)
    notebook_title: str = ""
    outline: list[str] = Field(default_factory=list)
    visible_section: str = ""
    history: list[dict[str, str]] = Field(default_factory=list)
    message: str = ""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/execute")
def execute(request: ExecuteRequest) -> dict[str, Any]:
    """Run one cell or ad-hoc code, guarding each session against concurrent runs."""
    lock = sessions.session_lock(request.notebook)
    if not lock.acquire(blocking=False):
        return _terminal_response("busy")
    try:
        return _execute_target(request)
    finally:
        lock.release()


@app.post("/reset")
def reset(request: ResetRequest) -> dict[str, str]:
    """Wipe the notebook's session namespace once any in-flight run finishes."""
    lock = sessions.session_lock(request.notebook)
    with lock:
        sessions.restart_kernel(request.notebook)
    return {"status": "ok"}


@app.get("/chat/settings")
def chat_settings() -> dict[str, str | bool]:
    """Chat provider/model summary; the API key is only ever reported as present."""
    return chat_config.settings_summary(ROOT)


@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """Stream tutor output as ``data: {json}`` events; always ends terminal-only."""
    settings = chat_config.load_chat_settings(ROOT)
    if request.mode == "elaborate":
        messages = elaborate_messages(request.section_markdown, request.context_cells)
    else:
        messages = chat_messages(
            notebook_title=request.notebook_title,
            outline=request.outline,
            visible_section=request.visible_section,
            history=request.history,
            message=request.message,
        )

    async def events() -> AsyncIterator[str]:
        errored = False
        async for chunk in stream_llm(settings, messages):
            errored = "error" in chunk
            yield f"data: {json.dumps(chunk)}\n\n"
        if not errored:
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")


def _execute_target(request: ExecuteRequest) -> dict[str, Any]:
    code = request.code
    if code is not None:
        try:
            sessions.resolve_notebook_path(request.path)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return _run_code(request.notebook, code)

    assert request.cell_index is not None  # validated: exactly one of the two
    try:
        source, cell_type, illustrative = sessions.load_cell_source(
            request.path, request.cell_index
        )
    except FileNotFoundError as exc:  # path resolves outside notebooks/
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:  # unparseable notebook JSON
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:  # cell index out of range
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if cell_type != "code":
        raise HTTPException(status_code=400, detail=f"cell {request.cell_index} is not a code cell")
    if illustrative:
        return _terminal_response("illustrative")
    return _run_code(request.notebook, source)


def _run_code(notebook: str, code: str) -> dict[str, Any]:
    """Run ``code`` on the session kernel; the kernel reports crashed children.

    ``get_kernel`` replaces a kernel whose subprocess already died, so an
    ``ExecResult`` of "crashed" means the death happened mid-run.
    """
    return _execution_response(sessions.get_kernel(notebook).execute(code))


def _execution_response(result: ExecResult) -> dict[str, Any]:
    return {
        "status": _HTTP_STATUS[result["status"]],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "traceback": result["traceback"],
        "elapsed_seconds": result["elapsed_seconds"],
    }


def _terminal_response(status: str, traceback: str | None = None) -> dict[str, Any]:
    """A result that did not run code: nothing elapsed, no output streams."""
    return {
        "status": status,
        "stdout": "",
        "stderr": "",
        "traceback": traceback,
        "elapsed_seconds": None,
    }
