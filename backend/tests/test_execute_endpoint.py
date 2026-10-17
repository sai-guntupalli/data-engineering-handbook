"""Tests for the /execute HTTP layer: session registry, status mapping, CORS."""

import threading
from collections.abc import Callable
from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend import sessions
from backend.main import app, ExecuteRequest

NOTEBOOK_PATH = "notebooks/topics/spark.ipynb"
# First runnable code cell of spark.ipynb (cell 13 is the first ILLUSTRATIVE one).
RUNNABLE_CELL_INDEX = 214
ILLUSTRATIVE_CELL_INDEX = 13


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
    source, illustrative = sessions.load_cell_source(NOTEBOOK_PATH, RUNNABLE_CELL_INDEX)

    assert source.startswith("shuffle_bytes = 200 * 1024 ** 3")
    assert illustrative is False


def test_load_cell_source_missing_source_key_is_empty_string(
    tmp_path: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    notebook = tmp_path / "cellless.ipynb"
    notebook.write_text('{"cells": [{"cell_type": "code"}]}', encoding="utf-8")
    monkeypatch.setattr(sessions, "NOTEBOOKS_DIR", tmp_path)

    source, illustrative = sessions.load_cell_source(str(notebook), 0)

    assert source == ""
    assert illustrative is False