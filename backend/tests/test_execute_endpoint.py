"""Tests for the /execute HTTP layer: session registry, status mapping, CORS."""

import json
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend import sessions
from backend.main import app, ExecuteRequest

NOTEBOOK_PATH = "notebooks/topics/spark.ipynb"

# The deterministic runnable cell: the shuffle-partition arithmetic cell. The
# viewer's literally-first runnable cell is the sample-data SparkSession
# bootstrap (Part 2), which needs Java, so the tests below pin this stdlib-only
# cell instead of an index that a future edit would silently move.
RUNNABLE_MARKER = "shuffle_bytes = 200 * 1024 ** 3"

# The first ILLUSTRATIVE code cell (the illustration marker doubles as the
# viewer's read-only badge; keep in step with lib/notebooks.ts).
ILLUSTRATIVE_MARKER = "# ILLUSTRATIVE"


def _cell_index_for_marker(path: str, marker: str, *, present: bool) -> int:
    raw = (Path(__file__).resolve().parents[2] / path).read_text(encoding="utf-8")
    cells = json.loads(raw).get("cells", [])
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source")
        text = "".join(source) if isinstance(source, list) else (source or "")
        if (marker in text) is present:
            return index
    raise AssertionError(f"no matching code cell found in {path}")


ILLUSTRATIVE_CELL_INDEX = _cell_index_for_marker(NOTEBOOK_PATH, ILLUSTRATIVE_MARKER, present=True)
RUNNABLE_CELL_INDEX = _cell_index_for_marker(NOTEBOOK_PATH, RUNNABLE_MARKER, present=True)


@pytest.fixture(autouse=True)
def close_test_kernels() -> Any:
    """Kill the kernel subprocesses this test spawned."""
    yield
    sessions.close_all()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _run_in_background(action: Callable[[], None]) -> threading.Thread:
    thread = threading.Thread(target=action)
    thread.start()
    return thread


class TestExecuteCell:
    def test_runnable_cell_returns_ok(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={"notebook": "t1", "path": NOTEBOOK_PATH, "cell_index": RUNNABLE_CELL_INDEX},
        )

        body = response.json()
        assert response.status_code == 200
        assert body["status"] == "ok"
        assert body["stdout"] == "target partitions: 1600\n"
        assert body["traceback"] is None
        assert body["elapsed_seconds"] > 0

    def test_illustrative_cell_returns_without_touching_kernel(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        kernel = sessions.get_kernel("t2")
        executed: list[str] = []
        monkeypatch.setattr(kernel, "execute", lambda code: executed.append(code))

        response = client.post(
            "/execute",
            json={"notebook": "t2", "path": NOTEBOOK_PATH, "cell_index": ILLUSTRATIVE_CELL_INDEX},
        )

        body = response.json()
        assert body["status"] == "illustrative"
        assert body["traceback"] is None
        assert body["elapsed_seconds"] is None
        assert executed == []

    def test_ad_hoc_code_persists_across_calls(self, client: TestClient) -> None:
        first = client.post("/execute", json={"notebook": "t3", "path": NOTEBOOK_PATH, "code": "y = 7"})
        second = client.post("/execute", json={"notebook": "t3", "path": NOTEBOOK_PATH, "code": "print(y * 2)"})

        assert first.json()["status"] == "ok"
        assert second.json()["status"] == "ok"
        assert second.json()["stdout"] == "14\n"

    def test_out_of_range_cell_index_returns_400(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={"notebook": "t4", "path": NOTEBOOK_PATH, "cell_index": 10_000},
        )

        assert response.status_code == 400

    def test_path_outside_notebooks_returns_404(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={"notebook": "t5", "path": "backend/kernel.py", "cell_index": 0},
        )

        assert response.status_code == 404

    def test_markdown_cell_target_returns_400(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={"notebook": "t10", "path": NOTEBOOK_PATH, "cell_index": 0},
        )

        assert response.status_code == 400
        assert "not a code cell" in response.json()["detail"]

    def test_non_dict_notebook_json_returns_400(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, client: TestClient
    ) -> None:
        notebook = tmp_path / "flat.json"
        notebook.write_text("[]", encoding="utf-8")
        monkeypatch.setattr(sessions, "NOTEBOOKS_DIR", tmp_path)

        response = client.post(
            "/execute",
            json={"notebook": "t-flat", "path": str(notebook), "cell_index": 0},
        )

        assert response.status_code == 400
        assert "not a notebook" in response.json()["detail"]


class TestKernelLifecycle:
    def test_dead_kernel_is_replaced_lazily(self, client: TestClient) -> None:
        kernel = sessions.get_kernel("t6")
        kernel._proc.kill()
        kernel._proc.wait(timeout=10)

        response = client.post(
            "/execute",
            json={"notebook": "t6", "path": NOTEBOOK_PATH, "code": "print('fresh')"},
        )

        body = response.json()
        assert body["status"] == "ok"
        assert body["stdout"] == "fresh\n"
        assert sessions.get_kernel("t6") is not kernel

    def test_kernel_death_mid_run_reports_crashed_then_next_request_recovers(
        self, client: TestClient
    ) -> None:
        killed = client.post(
            "/execute",
            json={"notebook": "t11", "path": NOTEBOOK_PATH, "code": "import os; os._exit(0)"},
        )

        killed_body = killed.json()
        assert killed_body["status"] == "crashed"
        assert "kernel process exited" in (killed_body["traceback"] or "")
        assert killed_body["elapsed_seconds"] is not None

        recovered = client.post(
            "/execute",
            json={"notebook": "t11", "path": NOTEBOOK_PATH, "code": "print('recovered')"},
        )

        assert recovered.json()["status"] == "ok"
        assert recovered.json()["stdout"] == "recovered\n"

    def test_in_flight_run_replies_busy_and_lets_first_finish(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        started = threading.Event()
        release = threading.Event()

        class BlockingKernel:
            def alive(self) -> bool:
                return True

            def execute(self, code: str) -> dict[str, Any]:
                started.set()
                release.wait(timeout=10)
                return {
                    "status": "ok",
                    "stdout": "first done\n",
                    "stderr": "",
                    "traceback": None,
                    "elapsed_seconds": 0.1,
                }

        fake_kernel = BlockingKernel()
        monkeypatch.setattr(sessions, "get_kernel", lambda notebook: fake_kernel)
        body_holder: dict[str, Any] = {}
        request = {"notebook": "t7", "path": NOTEBOOK_PATH, "code": "x = 1"}

        def run_first() -> None:
            with TestClient(app) as first_client:
                body_holder["first"] = first_client.post("/execute", json=request).json()

        thread = _run_in_background(run_first)
        assert started.wait(timeout=10)

        second = client.post("/execute", json=request)

        assert second.json()["status"] == "busy"
        assert second.json()["elapsed_seconds"] is None
        release.set()
        thread.join(timeout=10)
        assert body_holder["first"]["status"] == "ok"
        assert body_holder["first"]["stdout"] == "first done\n"


class _ScriptedKernel:
    """Fake Kernel answering execute() with one canned ExecResult."""

    def __init__(self, result: dict[str, Any]) -> None:
        self._result = result

    def alive(self) -> bool:
        return True

    def execute(self, code: str) -> dict[str, Any]:
        return self._result


INTERRUPTED_RESULT: dict[str, Any] = {
    "status": "interrupted",
    "stdout": "",
    "stderr": "",
    "traceback": "kernel did not respond to interrupt",
    "elapsed_seconds": 60.5,
}
CRASHED_RESULT: dict[str, Any] = {
    "status": "crashed",
    "stdout": "",
    "stderr": "",
    "traceback": "kernel process exited",
    "elapsed_seconds": 12.5,
}
ERROR_RESULT: dict[str, Any] = {
    "status": "error",
    "stdout": "",
    "stderr": "",
    "traceback": "ZeroDivisionError: division by zero",
    "elapsed_seconds": 0.2,
}


class TestKernelStatusMapping:
    @pytest.mark.parametrize(
        ("kernel_result", "http_status"),
        [
            (INTERRUPTED_RESULT, "timeout"),
            (CRASHED_RESULT, "crashed"),
            (ERROR_RESULT, "error"),
        ],
    )
    def test_kernel_status_travels_as(
        self,
        client: TestClient,
        monkeypatch: pytest.MonkeyPatch,
        kernel_result: dict[str, Any],
        http_status: str,
    ) -> None:
        monkeypatch.setattr(sessions, "get_kernel", lambda notebook: _ScriptedKernel(kernel_result))

        response = client.post(
            "/execute",
            json={"notebook": "t-map", "path": NOTEBOOK_PATH, "code": "x = 1"},
        )

        body = response.json()
        assert body["status"] == http_status
        assert body["traceback"] == kernel_result["traceback"]
        assert body["elapsed_seconds"] == kernel_result["elapsed_seconds"]


class TestReset:
    def test_reset_clears_session_namespace(self, client: TestClient) -> None:
        client.post("/execute", json={"notebook": "t8", "path": NOTEBOOK_PATH, "code": "wiped = 1"})
        reset = client.post("/reset", json={"notebook": "t8"})
        after = client.post("/execute", json={"notebook": "t8", "path": NOTEBOOK_PATH, "code": "print(wiped)"})

        assert reset.status_code == 200
        assert reset.json() == {"status": "ok"}
        assert after.json()["status"] == "error"
        assert "NameError" in (after.json()["traceback"] or "")


class TestHealthAndCors:
    def test_health(self, client: TestClient) -> None:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_preflight_from_allowed_origin_is_allowed(self, client: TestClient) -> None:
        response = client.options(
            "/execute",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )

        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_preflight_from_unknown_origin_is_denied(self, client: TestClient) -> None:
        response = client.options(
            "/execute",
            headers={
                "Origin": "http://evil.example",
                "Access-Control-Request-Method": "POST",
            },
        )

        assert "access-control-allow-origin" not in response.headers


class TestExecuteRequestValidation:
    def test_both_cell_index_and_code_is_rejected(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={
                "notebook": "t9",
                "path": NOTEBOOK_PATH,
                "cell_index": 214,
                "code": "x = 1",
            },
        )

        assert response.status_code == 400

    def test_neither_cell_index_nor_code_is_rejected(self, client: TestClient) -> None:
        response = client.post(
            "/execute",
            json={"notebook": "t9", "path": NOTEBOOK_PATH},
        )

        assert response.status_code == 400


def test_load_cell_source_joined_like_notebooks_ts() -> None:
    source, cell_type, illustrative = sessions.load_cell_source(NOTEBOOK_PATH, RUNNABLE_CELL_INDEX)

    assert source.startswith("shuffle_bytes = 200 * 1024 ** 3")
    assert cell_type == "code"
    assert illustrative is False


def test_load_cell_source_missing_source_key_is_empty_string(
    tmp_path: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    notebook = tmp_path / "cellless.ipynb"
    notebook.write_text('{"cells": [{"cell_type": "code"}]}', encoding="utf-8")
    monkeypatch.setattr(sessions, "NOTEBOOKS_DIR", tmp_path)

    source, cell_type, illustrative = sessions.load_cell_source(str(notebook), 0)

    assert source == ""
    assert cell_type == "code"
    assert illustrative is False
