#!/usr/bin/env python3
"""
Execute notebooks top to bottom, the way "Runtime -> Run all" does in Colab.

Every notebook under notebooks/ must run cleanly. Outputs are never written
back: notebooks are committed without outputs (see scripts/notebook_format.py).
With --output-dir, each notebook that runs cleanly is also saved, with trimmed
outputs, under that directory at its repository path. The site build reads
those copies to show results (see site/lib/notebooks.ts).

Usage:
  python scripts/run_notebooks.py                     # run every notebook
  python scripts/run_notebooks.py --jobs 4            # run four at a time
  python scripts/run_notebooks.py notebooks/topics/kafka/kafka.ipynb
  python scripts/run_notebooks.py --jobs 4 --output-dir build/executed

Requires the notebook tooling: uv sync --extra notebooks
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notebook_format import NOTEBOOKS_DIR, ROOT, notebook_paths  # noqa: E402

DEFAULT_CELL_TIMEOUT_SECONDS = 600

# Limits for outputs saved for the site: enough to show a result, small enough to keep pages light.
MAX_OUTPUT_LINES = 60
MAX_OUTPUT_CHARS = 6000
MAX_IMAGE_BASE64_CHARS = 400_000
SETUP_PREFIX = "# Setup:"
# Results that say nothing, such as the empty DataFrame that spark.sql("CREATE ...") returns.
EMPTY_RESULTS = {"DataFrame[]"}
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
# JVM and Spark log lines on stderr: log4j records, Spark 4 JSON logs, startup banners, progress bars.
# They carry no lesson content (and log4j lines include the machine's hostname), so the site drops them.
JVM_NOISE = re.compile(
    r"^(?:\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} (?:TRACE|DEBUG|INFO|WARN|ERROR) "
    r'|\{"ts": "[^"]*", "level": '
    r"|Using Spark's default log4j profile"
    r"|WARNING: Using incubator modules"
    r'|Setting default log level to "'
    r"|To adjust logging level use sc\.setLogLevel"
    r"|\[Stage \d+:"
    r"|Scaling row group sizes to )"
)


def _text(value: str | list[str]) -> str:
    return "".join(value) if isinstance(value, list) else value


def truncate_text(text: str) -> str:
    """Keep the first MAX_OUTPUT_LINES lines and MAX_OUTPUT_CHARS characters, and say what was cut."""
    lines = text.splitlines(keepends=True)
    kept = "".join(lines[:MAX_OUTPUT_LINES])
    if len(kept) > MAX_OUTPUT_CHARS:
        kept = kept[:MAX_OUTPUT_CHARS]
    if len(kept) == len(text):
        return text
    hidden = len(text[len(kept) :].splitlines())
    return kept.rstrip("\n") + f"\n… output trimmed ({hidden} more line{'s' if hidden != 1 else ''})\n"


def drop_jvm_noise(text: str) -> str:
    """Remove JVM and Spark log lines; a carriage return keeps only what the terminal would show last."""
    kept = [line.rsplit("\r", 1)[-1] for line in text.split("\n")]
    return "\n".join(line for line in kept if not JVM_NOISE.match(line))


def _trim_output(output: dict) -> dict | None:
    kind = output.get("output_type")
    if kind == "stream":
        text = ANSI_ESCAPE.sub("", _text(output.get("text", "")))
        if output.get("name") == "stderr":
            text = drop_jvm_noise(text)
        text = truncate_text(text)
        return {"output_type": "stream", "name": output.get("name", "stdout"), "text": text} if text.strip() else None
    if kind in ("execute_result", "display_data"):
        data = output.get("data", {})
        if "image/png" in data and len(_text(data["image/png"])) <= MAX_IMAGE_BASE64_CHARS:
            kept = {"image/png": _text(data["image/png"])}
        elif "text/plain" in data and _text(data["text/plain"]).strip() not in EMPTY_RESULTS:
            kept = {"text/plain": truncate_text(_text(data["text/plain"]))}
        else:
            return None
        trimmed = {"output_type": kind, "data": kept, "metadata": {}}
        if kind == "execute_result":
            trimmed["execution_count"] = output.get("execution_count")
        return trimmed
    if kind == "error":
        return {
            "output_type": "error",
            "ename": output.get("ename", ""),
            "evalue": output.get("evalue", ""),
            "traceback": [],
        }
    return None


def trim_outputs(notebook: dict) -> dict:
    """Outputs as the site shows them: no setup-cell noise, no HTML, no ANSI colour, long text cut short."""
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if _text(cell.get("source", "")).lstrip().startswith(SETUP_PREFIX):
            cell["outputs"] = []
            continue
        cell["outputs"] = [kept for output in cell.get("outputs", []) if (kept := _trim_output(output)) is not None]
    return notebook


def run_one(path: Path, timeout: int, output_dir: Path | None = None) -> tuple[str, str | None, float]:
    """Execute one notebook; return (relpath, error or None, seconds). Save a trimmed copy to output_dir."""
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
    if output_dir is not None:
        target = output_dir / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nbformat.from_dict(trim_outputs(json.loads(json.dumps(notebook)))), target)
    return relpath, None, time.monotonic() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="notebooks to run (default: all under notebooks/)")
    parser.add_argument("--jobs", type=int, default=1, help="notebooks to execute in parallel")
    parser.add_argument("--timeout", type=int, default=DEFAULT_CELL_TIMEOUT_SECONDS, help="per-cell timeout (s)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="also save each notebook that runs cleanly, with trimmed outputs, under this directory",
    )
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
        output_dir = args.output_dir.resolve() if args.output_dir else None
        futures = [pool.submit(run_one, path, args.timeout, output_dir) for path in paths]
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
