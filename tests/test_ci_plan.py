"""Unit tests for the CI planner (scripts/ci_plan.py)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ci_plan  # noqa: E402

SQL_DRILLS = "notebooks/topics/sql/sql-13-interview-drills.ipynb"
PYSPARK_PRACTICE = "notebooks/topics/pyspark/pyspark-practice-09-joins.ipynb"
PLAIN = "notebooks/topics/kafka/kafka.ipynb"


def test_shared_tooling_runs_everything():
    work = ci_plan.plan(["uv.lock"])
    assert work == ci_plan.plan(None)
    assert len(work["fixtures"]) == len(ci_plan.fixtures())
    assert PLAIN in work["notebooks"]


def test_unrelated_changes_run_nothing():
    assert ci_plan.plan(["README.md", "site/lib/learning-map.ts"]) == {"notebooks": [], "fixtures": []}


def test_changed_plain_notebook_runs_only_itself():
    assert ci_plan.plan([PLAIN, "README.md"]) == {"notebooks": [PLAIN], "fixtures": []}


def test_challenge_notebook_is_executed_by_its_verifier_only():
    work = ci_plan.plan([PYSPARK_PRACTICE])
    assert work == {"notebooks": [], "fixtures": ["pyspark-practice-09-joins"]}


def test_fixture_with_hidden_cells_also_gets_a_plain_run():
    # sql-13's fixture restores removed cells, so the published notebook must still run on its own.
    assert ci_plan.plan([SQL_DRILLS]) == {"notebooks": [SQL_DRILLS], "fixtures": ["sql-13-interview-drills"]}


def test_changed_fixture_verifies_its_notebook():
    work = ci_plan.plan(["tests/fixtures/challenge-checks/pyspark-practice-09-joins.json"])
    assert work == {"notebooks": [], "fixtures": ["pyspark-practice-09-joins"]}


def test_deleted_notebooks_are_ignored():
    assert ci_plan.plan(["notebooks/topics/sql/sql-99-gone.ipynb"]) == {"notebooks": [], "fixtures": []}


def test_shards_are_balanced_and_cover_all_work():
    work = ci_plan.plan(None)
    shards = ci_plan.shards(work, 4)
    assert len(shards) == 4
    assert sorted(" ".join(s["notebooks"] for s in shards).split()) == work["notebooks"]
    assert sorted(" ".join(s["fixtures"] for s in shards).split()) == work["fixtures"]
    loads = [int(s["estimate_seconds"]) for s in shards]
    assert max(loads) - min(loads) <= 0.1 * max(loads)


def test_small_work_uses_fewer_shards():
    shards = ci_plan.shards({"notebooks": [PLAIN], "fixtures": []}, 4)
    assert [s["notebooks"] for s in shards] == [PLAIN]
    assert ci_plan.shards({"notebooks": [], "fixtures": []}, 4) == []
