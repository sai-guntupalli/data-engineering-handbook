"""Kernel subprocess: executes code requests over a line-delimited JSON protocol.

Each request line is ``{"id": <int>, "code": <str>}``; each response line is
``{"id", "status", "stdout", "stderr", "traceback", "elapsed_seconds"}``. The
namespace is one dict persisted across requests. A run whose SIGINT interrupt
raises ``KeyboardInterrupt`` inside ``exec`` replies ``status: "interrupted"``,
so the controller's wait always ends with a response.
"""

import contextlib
import io
import json
import sys
import time
import traceback


def run_requests() -> None:
    """Read requests from stdin and write one response line per request to stdout."""
    namespace: dict = {}

    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            _run_one(json.loads(line), namespace)
    except KeyboardInterrupt:
        # SIGINT while idle between requests: no response is awaited, exit quietly.
        return


def _run_one(request: dict, namespace: dict) -> None:
    started = time.perf_counter()
    stdout = io.StringIO()
    stderr = io.StringIO()
    status = "ok"
    tb = None
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            # exec of request code is the kernel's whole purpose.
            exec(request["code"], namespace)
    except KeyboardInterrupt:
        status = "interrupted"
    except BaseException:  # user code may raise anything at all
        status = "error"
        tb = traceback.format_exc()
    elapsed_seconds = time.perf_counter() - started

    response = {
        "id": request["id"],
        "status": status,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "traceback": tb,
        "elapsed_seconds": elapsed_seconds,
    }
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    run_requests()