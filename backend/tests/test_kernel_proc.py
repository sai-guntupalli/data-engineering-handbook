"""Tests for the persistent Python kernel subprocess protocol."""

import pytest

from backend.kernel import Kernel


class TestKernel:
    @pytest.fixture
    def kernel(self) -> Kernel:
        kernel = Kernel()
        yield kernel
        kernel.close()

    def test_state_persists_across_executions(self, kernel: Kernel) -> None:
        kernel.execute("x = 40")

        result = kernel.execute("print(x + 2)")

        assert result["status"] == "ok"
        assert result["stdout"] == "42\n"

    def test_captures_stdout_and_stderr(self, kernel: Kernel) -> None:
        result = kernel.execute('print("out"); import sys; print("err", file=sys.stderr)')

        assert result["status"] == "ok"
        assert result["stdout"] == "out\n"
        assert result["stderr"] == "err\n"

    def test_error_returns_traceback(self, kernel: Kernel) -> None:
        result = kernel.execute("1 / 0")

        assert result["status"] == "error"
        assert result["traceback"] is not None
        assert "ZeroDivisionError" in result["traceback"]

    def test_timeout_interrupts_and_kernel_recovers_without_restart(
        self, kernel: Kernel
    ) -> None:
        blocked = Kernel(timeout_seconds=0.5)

        try:
            assert blocked.alive()

            result = blocked.execute("import time; time.sleep(5)")

            assert result["status"] == "interrupted"
            assert blocked.alive()

            follow_up = blocked.execute('print("alive")')

            assert follow_up["status"] == "ok"
            assert follow_up["stdout"] == "alive\n"
        finally:
            blocked.close()

    def test_oversized_output_is_truncated(self, kernel: Kernel) -> None:
        result = kernel.execute('print("a" * 30000)')

        assert result["status"] == "ok"
        assert len(result["stdout"]) <= 20000
        assert "... [truncated]" in result["stdout"]