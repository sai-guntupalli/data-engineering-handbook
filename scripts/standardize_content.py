#!/usr/bin/env python3
"""
Apply safe terminology and whitespace standardization across the markdown docs.

This is intentionally conservative: it fixes casing and legacy spelling drift that
appears across many older Q&A files without rewriting the authorial structure.

Usage:
  python3 scripts/standardize_content.py
  python3 scripts/standardize_content.py --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"


REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bMapreduce\b"), "MapReduce"),
    (re.compile(r"\bmapreduce\b"), "MapReduce"),
    (re.compile(r"\bMap reduce\b"), "MapReduce"),
    (re.compile(r"\bmap reduce\b"), "MapReduce"),
    (re.compile(r"\bMLib\b"), "MLlib"),
    (re.compile(r"\bMlib\b"), "MLlib"),
    (re.compile(r"\bRdd\b"), "RDD"),
    (re.compile(r"\bRDDs\b"), "RDDs"),
    (re.compile(r"\bDstream\b"), "DStream"),
    (re.compile(r"\bDstreams\b"), "DStreams"),
    (re.compile(r"\bHbase\b"), "HBase"),
    (re.compile(r"\bBigquery\b"), "BigQuery"),
    (re.compile(r"\bGithub\b"), "GitHub"),
    (re.compile(r"\bDatawarehouse\b"), "data warehouse"),
    (re.compile(r"\bData warehousing\b"), "Data warehousing"),
    (re.compile(r"\bSparksql\b"), "Spark SQL"),
    (re.compile(r"\bSparkSQL\b"), "Spark SQL"),
]


def protect_markdown_link_targets(text: str) -> tuple[str, list[str]]:
    targets: list[str] = []

    def replace(match: re.Match[str]) -> str:
        targets.append(match.group(0))
        return f"@@LINK_TARGET_{len(targets) - 1}@@"

    return re.sub(r"\]\([^)]+\)", replace, text), targets


def restore_markdown_link_targets(text: str, targets: list[str]) -> str:
    for index, target in enumerate(targets):
        text = text.replace(f"@@LINK_TARGET_{index}@@", target)
    return text


def standardize_text(text: str) -> str:
    updated = text.replace("\r\n", "\n")
    updated, link_targets = protect_markdown_link_targets(updated)
    for pattern, replacement in REPLACEMENTS:
        updated = pattern.sub(replacement, updated)
    updated = restore_markdown_link_targets(updated, link_targets)

    lines = [line.rstrip() for line in updated.split("\n")]
    collapsed: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            collapsed.append(line)
        else:
            blank_count += 1
            if blank_count <= 2:
                collapsed.append("")

    return "\n".join(collapsed).rstrip() + "\n"


def markdown_files() -> list[Path]:
    return [*sorted(CONTENT_DIR.glob("*.md")), ROOT / "README.md", ROOT / "CONTRIBUTING.md"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if any file would change")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        updated = standardize_text(original)
        if updated == original:
            continue
        changed.append(path)
        if not args.check:
            path.write_text(updated, encoding="utf-8")

    if args.check and changed:
        print("Content standardization needed:", file=sys.stderr)
        for path in changed:
            print(f"- {path.relative_to(ROOT)}", file=sys.stderr)
        return 1

    if changed:
        print(f"Standardized {len(changed)} file(s).")
    else:
        print("Content is already standardized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
