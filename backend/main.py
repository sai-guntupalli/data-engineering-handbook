"""Local interactive viewer backend.

``POST /execute`` runs a notebook cell (or ad-hoc code) in a per-notebook
kernel session; ``POST /reset`` wipes a session's namespace; ``GET /health``
is the liveness probe. Execution results travel in the body with status 200;
only request-shape problems use HTTP error codes.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator

from backend import sessions
from backend.kernel import ExecResult

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

# Kernel statuses map onto the HTTP-layer vocabulary: an interrupt-based
# timeout is communicated as "timeout", and the traceback says what happened.
_HTTP_STATUS = {"ok": "ok", "error": "error", "interrupted": "timeout"}


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
        source, illustrative = sessions.load_cell_source(request.path, request.cell_index)
    except FileNotFoundError as exc:  # path resolves outside notebooks/
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:  # unparseable notebook JSON
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:  # cell index out of range
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if illustrative:
        return _terminal_response("illustrative")
    return _run_code(request.notebook, source)


def _run_code(notebook: str, code: str) -> dict[str, Any]:
    kernel = sessions.get_kernel(notebook)
    if not kernel.alive():
        return _terminal_response("crashed", "kernel process exited")
    return _execution_response(kernel.execute(code))


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