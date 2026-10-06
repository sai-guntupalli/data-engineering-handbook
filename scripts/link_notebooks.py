#!/usr/bin/env python3
"""
Add a link to the matching notebook at the top of every topic document.

Each content/<topic>.md gets one line directly under its title:

    **Notebook:** [`notebooks/topics/<topic>.ipynb`](../notebooks/topics/<topic>.ipynb) - ...

The relative path works in every context:
  * on GitHub, from content/<topic>.md it points at the repository notebook;
  * in the Next.js app, the topic page exposes the same notebook through the
    `/notebook-files/topics/<topic>.ipynb` download route.

Usage:
  python3 scripts/link_notebooks.py          # insert or refresh the links
  python3 scripts/link_notebooks.py --check  # fail if a link is missing (CI-safe)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
TOPIC_NOTEBOOKS = ROOT / "notebooks" / "topics"

MARKER = "**Notebook:**"


def notebook_line(slug: str) -> str:
    target = f"../notebooks/topics/{slug}.ipynb"
    return f"{MARKER} [`notebooks/topics/{slug}.ipynb`]({target}) - runnable version of this topic with self-checking exercises."


def _h1_index(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if line.startswith("# "):
            return index
    return None


def apply_link(text: str, slug: str) -> str:
    """Return the document with exactly one notebook link under its title."""
    lines = [line for line in text.splitlines() if MARKER not in line]

    h1 = _h1_index(lines)
    if h1 is None:
        raise ValueError(f"{slug}.md has no '# Title' heading")

    rest = lines[h1 + 1:]
    while rest and not rest[0].strip():
        rest.pop(0)

    rebuilt = lines[: h1 + 1] + ["", notebook_line(slug), ""] + rest
    return "\n".join(rebuilt).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify every document links its notebook")
    args = parser.parse_args()

    documents = sorted(path for path in CONTENT_DIR.glob("*.md") if path.name != "full.md")
    changed: list[str] = []
    missing: list[str] = []

    for path in documents:
        slug = path.stem
        if not (TOPIC_NOTEBOOKS / f"{slug}.ipynb").exists():
            print(f"note: no notebook for {path.name}, skipping", file=sys.stderr)
            continue

        original = path.read_text(encoding="utf-8")
        if MARKER in original and notebook_line(slug) in original:
            continue

        updated = apply_link(original, slug)
        if args.check:
            missing.append(path.name)
            continue

        path.write_text(updated, encoding="utf-8")
        changed.append(path.name)

    if args.check:
        if missing:
            print("These documents are missing their notebook link: " + ", ".join(missing), file=sys.stderr)
            print("Run: python3 scripts/link_notebooks.py", file=sys.stderr)
            return 1
        print(f"All {len(documents)} topic documents link their notebook.")
        return 0

    if changed:
        print(f"Updated {len(changed)} document(s): " + ", ".join(changed))
    else:
        print("All topic documents already link their notebook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
