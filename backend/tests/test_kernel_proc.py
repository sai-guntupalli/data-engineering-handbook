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

    def test_grace_expiry_reports_interrupted_and_auto_resets(self) -> None:
        # Code that ignores SIGINT wedges the kernel: the timeout's interrupt
        # never lands, the grace expires, and the kernel must come back ready.
        wedged = Kernel(timeout_seconds=0.5, interrupt_grace_seconds=0.5)

        try:
            result = wedged.execute(
                "import signal, time; signal.signal(signal.SIGINT, signal.SIG_IGN); time.sleep(60)"
            )

            assert result["status"] == "interrupted"
            assert "kernel was reset" in (result["traceback"] or "")

            follow_up = wedged.execute("print('ok')")

            assert follow_up["status"] == "ok"
            assert follow_up["stdout"] == "ok\n"
        finally:
            wedged.close()

    def test_oversized_output_is_truncated(self, kernel: Kernel) -> None:
        result = kernel.execute('print("a" * 30000)')

        assert result["status"] == "ok"
        assert len(result["stdout"]) <= 20000
        assert "... [truncated]" in result["stdout"]

    def test_non_protocol_stdout_line_does_not_kill_reader(self) -> None:
        kernel = Kernel(timeout_seconds=2.0)

        try:
            first = kernel.execute('import sys; print("42", file=sys.__stdout__)')

            assert first["status"] == "ok"
            assert kernel.alive()

            second = kernel.execute('print("after")')

            assert second["status"] == "ok"
            assert second["stdout"] == "after\n"
        finally:
            kernel.close()

    def test_child_that_dies_mid_run_reports_crashed(self) -> None:
        kernel = Kernel()

        try:
            result = kernel.execute("import os; os._exit(0)")

            assert result["status"] == "crashed"
            assert "kernel process exited" in (result["traceback"] or "")
            assert result["stdout"] == ""
        finally:
            kernel.close()

    def test_reset_recovers_after_kernel_death(self, kernel: Kernel) -> None:
        kernel.execute("import os; os._exit(0)")
        assert not kernel.alive()

        kernel.reset()
        result = kernel.execute('print("back")')

        assert result["status"] == "ok"
        assert result["stdout"] == "back\n"
