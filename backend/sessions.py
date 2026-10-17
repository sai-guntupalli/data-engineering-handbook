"""Per-notebook kernel registry and notebook cell loading.

The registry keeps one :class:`Kernel` subprocess per notebook slug for the
lifetime of the server. A kernel whose subprocess has died is replaced lazily
the next time :func:`get_kernel` is called for that notebook.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from backend.kernel import Kernel

_REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = _REPO_ROOT / "notebooks"

_KERNELS: dict[str, Kernel] = {}
_LOCKS: dict[str, threading.Lock] = {}
_REGISTRY_LOCK = threading.Lock()

# Marker of a cell that needs a platform (or paid engine) to run locally. Must
# stay in step with lib/notebooks.ts, which counts cells with the same marker.
ILLUSTRATIVE_MARKER = "# ILLUSTRATIVE"


def get_kernel(notebook: str) -> Kernel:
    """Return the notebook's live kernel, creating or replacing it lazily."""
    with _REGISTRY_LOCK:
        kernel = _KERNELS.get(notebook)
        if kernel is None or not kernel.alive():
            kernel = Kernel()
            _KERNELS[notebook] = kernel
        return kernel


def restart_kernel(notebook: str) -> Kernel:
    """Reset the notebook's kernel in place, or create one if there is none."""
    with _REGISTRY_LOCK:
        kernel = _KERNELS.get(notebook)
        if kernel is None:
            kernel = Kernel()
            _KERNELS[notebook] = kernel
        else:
            kernel.reset()
        return kernel


def session_lock(notebook: str) -> threading.Lock:
    """Return the per-notebook execution lock, creating it on first use."""
    with _REGISTRY_LOCK:
        lock = _LOCKS.get(notebook)
        if lock is None:
            lock = threading.Lock()
            _LOCKS[notebook] = lock
        return lock


def close_all() -> None:
    """Terminate every registered kernel (used at teardown/shutdown)."""
    with _REGISTRY_LOCK:
        kernels = list(_KERNELS.values())
        _KERNELS.clear()
    for kernel in kernels:
        kernel.close()


def resolve_notebook_path(notebook_path: str) -> Path:
    """Resolve a repo-relative (or absolute-but-inside-) notebook path.

    Raises ``FileNotFoundError`` when the path escapes ``notebooks/``.
    """
    candidate = Path(notebook_path)
    if not candidate.is_absolute():
        candidate = _REPO_ROOT / candidate
    resolved = candidate.resolve()
    if not resolved.is_relative_to(NOTEBOOKS_DIR):
        raise FileNotFoundError(f"notebook path is outside notebooks/: {notebook_path}")
    return resolved


def load_cell_source(notebook_path: str, index: int) -> tuple[str, str, bool]:
    """Return ``(source, cell_type, is_illustrative)`` for cell ``index`` of a notebook.

    ``index`` addresses the raw ``cells`` array — the same indexing the viewer
    frontend uses. Cell sources are joined like ``lib/notebooks.ts`` does, so a
    cell whose ``source`` key is missing counts as empty, and a cell without a
    ``cell_type`` counts as ``"markdown"`` (the TS reader's default). Raises
    ``KeyError`` when ``index`` is out of range and ``ValueError`` when the
    notebook JSON is unparseable.
    """
    notebook = json.loads(resolve_notebook_path(notebook_path).read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    if not 0 <= index < len(cells):
        raise KeyError(f"cell index {index} out of range (notebook has {len(cells)} cells)")
    cell = cells[index]
    source = _cell_source(cell)
    return source, cell.get("cell_type", "markdown"), ILLUSTRATIVE_MARKER in source


def _cell_source(cell: dict) -> str:
    source = cell.get("source")
    if isinstance(source, list):
        return "".join(source)
    if isinstance(source, str):
        return source
    return ""
