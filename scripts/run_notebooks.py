#!/usr/bin/env python3
"""
Execute notebooks top to bottom, the way "Runtime -> Run all" does in Colab.

Every notebook under notebooks/ must run cleanly. Outputs are never written
back: notebooks are committed without outputs (see scripts/notebook_format.py).

Usage:
  python scripts/run_notebooks.py                     # run every notebook
  python scripts/run_notebooks.py --jobs 4            # run four at a time
  python scripts/run_notebooks.py notebooks/topics/kafka/kafka.ipynb

Requires the notebook tooling: uv sync --extra notebooks
"""

from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_format import NOTEBOOKS_DIR, ROOT, notebook_paths  # noqa: E402

DEFAULT_CELL_TIMEOUT_SECONDS = 600


def run_one(path: Path, timeout: int) -> tuple[str, str | None, float]:
    """Execute one notebook; return (relpath, error or None, seconds)."""
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    relpath = path.relative_to(ROOT).as_posix()
    started = time.monotonic()
    try:
        notebook = nbformat.read(path, as_version=4)
        NotebookClient(
            notebook,
            timeout=timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        ).execute()
    except CellExecutionError as exc:
        summary = str(exc).strip().splitlines()
        return relpath, summary[-1] if summary else "cell execution failed", time.monotonic() - started
    except Exception as exc:  # kernel start-up failures, timeouts, unreadable files
        return relpath, f"{type(exc).__name__}: {exc}", time.monotonic() - started
    return relpath, None, time.monotonic() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="notebooks to run (default: all under notebooks/)")
    parser.add_argument("--jobs", type=int, default=1, help="notebooks to execute in parallel")
    parser.add_argument("--timeout", type=int, default=DEFAULT_CELL_TIMEOUT_SECONDS, help="per-cell timeout (s)")
    args = parser.parse_args()

    try:
        import nbclient  # noqa: F401
        import nbformat  # noqa: F401
    except ImportError:
        print("Notebook tooling is missing: uv sync --extra notebooks", file=sys.stderr)
        return 1

    paths = notebook_paths(args.files)
    if not paths:
        print(f"No notebooks found in {NOTEBOOKS_DIR}", file=sys.stderr)
        return 1

    failures: list[tuple[str, str]] = []
    with ProcessPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_one, path, args.timeout) for path in paths]
        for future in futures:
            relpath, error, seconds = future.result()
            if error:
                failures.append((relpath, error))
                print(f"FAIL {relpath} ({seconds:.0f}s): {error}", flush=True)
            else:
                print(f"OK   {relpath} ({seconds:.0f}s)", flush=True)

    if failures:
        print(f"\n{len(failures)} of {len(paths)} notebook(s) failed:", file=sys.stderr)
        for relpath, error in failures:
            print(f"  - {relpath}: {error}", file=sys.stderr)
        return 1
    print(f"\nAll {len(paths)} notebook(s) ran cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
