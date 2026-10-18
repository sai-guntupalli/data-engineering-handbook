"""Controller for the kernel subprocess.

Spawns ``backend/kernel_proc.py`` as a child of ``sys.executable`` and speaks
the line-delimited JSON protocol on its stdin/stdout. Output truncation lives
here: it is the single truncation point between the kernel and the HTTP layer.
"""

import itertools
import json
import queue
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Literal, TypedDict

_KERNEL_PROC_PATH = Path(__file__).with_name("kernel_proc.py")
MAX_OUTPUT_CHARS = 20_000
_TRUNCATION_MARKER = "\n... [truncated]"
INTERRUPT_GRACE_SECONDS = 5.0

_DEAD_TRACEBACK = "kernel process exited"


# "crashed" marks a dead child: the execute that observed the death carries it
# (traceback _DEAD_TRACEBACK); the next execute gets a fresh kernel.
_ResultStatus = Literal["ok", "error", "interrupted", "crashed"]


class ExecResult(TypedDict):
    status: _ResultStatus
    stdout: str
    stderr: str
    traceback: str | None
    elapsed_seconds: float


def _truncate(value: str) -> str:
    """Keep at most MAX_OUTPUT_CHARS characters, marker-appended when cut."""
    if len(value) > MAX_OUTPUT_CHARS:
        value = value[: MAX_OUTPUT_CHARS - len(_TRUNCATION_MARKER)]
        value += _TRUNCATION_MARKER
    return value


def _parse_response(line: str) -> dict | None:
    """Parse one stdout line as a protocol response, or return None.

    Lines that are not well-formed responses are skipped rather than killing
    the reader: user code can print JSON to the real stdout
    (``print(42, file=sys.__stdout__)``), which shares this pipe with us.
    """
    try:
        response = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(response, dict):
        return None
    if response.get("status") not in ("ok", "error", "interrupted"):
        return None
    if not isinstance(response.get("stdout"), str) or not isinstance(response.get("stderr"), str):
        return None
    if response.get("traceback") is not None and not isinstance(response.get("traceback"), str):
        return None
    try:
        response["id"] = int(response["id"])
        response["elapsed_seconds"] = float(response["elapsed_seconds"])
    except (KeyError, TypeError, ValueError):
        return None
    return response


class Kernel:
    """A persistent Python kernel subprocess with an interrupt-based timeout."""

    def __init__(
        self,
        timeout_seconds: float = 60.0,
        interrupt_grace_seconds: float = INTERRUPT_GRACE_SECONDS,
    ) -> None:
        self._timeout_seconds = timeout_seconds
        self._interrupt_grace_seconds = interrupt_grace_seconds
        self._request_ids = itertools.count()
        self._waiters: dict[int, queue.Queue[dict | None]] = {}
        self._waiters_lock = threading.Lock()
        self._proc = self._spawn()
        self._reader = self._start_reader()

    def execute(self, code: str) -> ExecResult:
        """Run ``code`` in the persistent namespace, interrupting on timeout."""
        started = time.monotonic()
        request_id = next(self._request_ids)
        response_queue: queue.Queue[dict | None] = queue.Queue()

        try:
            with self._waiters_lock:
                self._waiters[request_id] = response_queue

            try:
                self._write_request(request_id, code)
            except (OSError, ValueError):
                return _synthesized_result("crashed", _DEAD_TRACEBACK, started)

            try:
                response = response_queue.get(timeout=self._timeout_seconds)
            except queue.Empty:
                self._proc.send_signal(signal.SIGINT)
                try:
                    response = response_queue.get(timeout=self._interrupt_grace_seconds)
                except queue.Empty:
                    # The interrupt never landed: the namespace is wedged, so
                    # the timed-out kernel resets for the next cell instead of
                    # staying busy for good.
                    self.reset()
                    traceback = (
                        f"cell timed out after {self._timeout_seconds}s; "
                        "interrupt did not respond; kernel was reset"
                    )
                    return _synthesized_result("interrupted", traceback, started)
            if response is None:
                return _synthesized_result("crashed", _DEAD_TRACEBACK, started)
        finally:
            with self._waiters_lock:
                self._waiters.pop(request_id, None)

        return self._collect(response)

    def alive(self) -> bool:
        return self._proc.poll() is None

    def reset(self) -> None:
        """Kill the subprocess and start a fresh one with an empty namespace."""
        self._terminate()
        self._proc = self._spawn()
        self._reader = self._start_reader()

    def close(self) -> None:
        self._terminate()

    def _spawn(self) -> subprocess.Popen[str]:
        return subprocess.Popen(
            [sys.executable, str(_KERNEL_PROC_PATH)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

    def _start_reader(self) -> threading.Thread:
        proc = self._proc
        reader = threading.Thread(
            target=self._read_responses, args=(proc,), name="kernel-reader", daemon=True
        )
        reader.start()
        return reader

    def _write_request(self, request_id: int, code: str) -> None:
        assert self._proc.stdin is not None  # created with stdin=PIPE
        self._proc.stdin.write(json.dumps({"id": request_id, "code": code}) + "\n")
        self._proc.stdin.flush()

    def _read_responses(self, proc: subprocess.Popen[str]) -> None:
        """Forward each parsed response to the waiter matching its request id."""
        assert proc.stdout is not None  # created with stdout=PIPE
        for line in proc.stdout:
            response = _parse_response(line)
            if response is None:
                continue
            with self._waiters_lock:
                waiter = self._waiters.pop(response["id"], None)
            if waiter is not None:
                waiter.put(response)

        # EOF: the subprocess is gone. Release anyone still waiting for it, but
        # never for one replaced by reset(): a newer reader owns those waiters.
        with self._waiters_lock:
            if self._proc is not proc:
                return
            waiters = list(self._waiters.values())
            self._waiters.clear()
        for waiter in waiters:
            waiter.put(None)

    def _collect(self, response: dict) -> ExecResult:
        return ExecResult(
            status=response["status"],
            stdout=_truncate(response["stdout"]),
            stderr=_truncate(response["stderr"]),
            traceback=response["traceback"],
            elapsed_seconds=response["elapsed_seconds"],
        )

    def _terminate(self) -> None:
        if self._proc.poll() is None:
            self._proc.kill()
        try:
            self._proc.wait(timeout=INTERRUPT_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            pass
        for stream in (self._proc.stdin, self._proc.stdout):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass


def _synthesized_result(status: _ResultStatus, traceback_text: str, started: float) -> ExecResult:
    """Build a result without a child response (dead child or dead interrupt)."""
    return ExecResult(
        status=status,
        stdout="",
        stderr="",
        traceback=traceback_text,
        elapsed_seconds=time.monotonic() - started,
    )
