#!/usr/bin/env python3
"""
Decide which notebooks and challenge fixtures CI executes, and split them into balanced shards.

Pull requests run only what they touch: changed notebooks, plus the challenge verification of changed notebooks
and changed fixtures. A change to shared tooling (dependencies, the runner, the verifier, the workflow) runs
everything, and so does every push to master.

A notebook with a challenge fixture that hides no extra cells is executed only by the challenge verifier: the
verifier runs the same notebook top to bottom with the hidden answers restored, so a plain run would repeat it.

Usage:
  python scripts/ci_plan.py --base origin/master          # affected work for a pull request
  python scripts/ci_plan.py --all                         # everything
  python scripts/ci_plan.py --all --shards 4 --github-output "$GITHUB_OUTPUT"

Prints a JSON plan; with --github-output, also writes `matrix` and `has_work` for GitHub Actions.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = "notebooks/"
FIXTURES = "tests/fixtures/challenge-checks/"
DURATIONS = ROOT / "scripts/ci_notebook_seconds.json"
DEFAULT_SECONDS = 60  # notebooks without a measured duration (new ones)

# Changes here can affect any notebook, so they run everything.
SHARED = (
    "pyproject.toml",
    "uv.lock",
    "scripts/run_notebooks.py",
    "scripts/verify_challenge_answers.py",
    "scripts/ci_plan.py",
    ".github/workflows/repo-checks.yml",
)


def changed_files(base: str) -> list[str]:
    """Files that differ between the merge base with `base` and HEAD (added, modified, renamed or deleted)."""
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    return [line for line in out.splitlines() if line]


def fixtures() -> dict[str, dict]:
    """Challenge fixtures by stem."""
    return {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / FIXTURES).glob("*.json"))}


def all_notebooks() -> list[str]:
    return sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / NOTEBOOKS).rglob("*.ipynb"))


def plan(changed: list[str] | None) -> dict[str, list[str]]:
    """`notebooks` to execute and challenge `fixtures` to verify. `changed=None` means everything."""
    fx = fixtures()
    by_notebook = {f["notebook"]: stem for stem, f in fx.items()}
    existing = set(all_notebooks())

    if changed is None or any(path in SHARED for path in changed):
        notebooks, stems = sorted(existing), sorted(fx)
    else:
        notebooks = sorted(p for p in changed if p.startswith(NOTEBOOKS) and p.endswith(".ipynb") and p in existing)
        stems = {by_notebook[p] for p in notebooks if p in by_notebook}
        stems |= {Path(p).stem for p in changed if p.startswith(FIXTURES) and Path(p).stem in fx}
        stems = sorted(s for s in stems if fx[s]["notebook"] in existing)

    # The verifier executes these notebooks in full, so a plain run would only repeat it.
    covered = {fx[s]["notebook"] for s in stems if not fx[s]["removed_cells"]}
    return {"notebooks": [p for p in notebooks if p not in covered], "fixtures": stems}


def shards(work: dict[str, list[str]], count: int) -> list[dict[str, str]]:
    """Split the work into at most `count` shards of similar total duration (longest first, onto the lightest)."""
    seconds = json.loads(DURATIONS.read_text()) if DURATIONS.exists() else {}
    fx = fixtures()
    items = [("notebook", p, seconds.get(p, DEFAULT_SECONDS)) for p in work["notebooks"]]
    # A challenge verification executes its notebook once more, with checks.
    items += [("fixture", s, seconds.get(fx[s]["notebook"], DEFAULT_SECONDS) * 1.2) for s in work["fixtures"]]
    if not items:
        return []
    buckets = [{"notebook": [], "fixture": [], "load": 0.0} for _ in range(min(count, len(items)))]
    for kind, name, cost in sorted(items, key=lambda item: -item[2]):
        lightest = min(buckets, key=lambda b: b["load"])
        lightest[kind].append(name)
        lightest["load"] += cost
    return [
        {
            "name": f"{i + 1} of {len(buckets)}",
            "notebooks": " ".join(sorted(b["notebook"])),
            "fixtures": " ".join(sorted(b["fixture"])),
            "estimate_seconds": str(round(b["load"])),
        }
        for i, b in enumerate(buckets)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--base", help="git ref to diff against (pull requests)")
    scope.add_argument("--all", action="store_true", help="plan every notebook and fixture")
    parser.add_argument("--shards", type=int, default=4, help="maximum number of parallel shards")
    parser.add_argument("--github-output", help="append `matrix` and `has_work` to this GitHub Actions output file")
    args = parser.parse_args()

    work = plan(None if args.all else changed_files(args.base))
    matrix = shards(work, args.shards)
    print(json.dumps({"work": work, "shards": matrix}, indent=1))
    if args.github_output:
        with open(args.github_output, "a") as out:
            out.write(f"matrix={json.dumps({'include': matrix})}\n")
            out.write(f"has_work={'true' if matrix else 'false'}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
