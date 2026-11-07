# Progress

**Current Status**: All 57 notebooks are Colab-runnable, lean, and executed by CI (green on PR #28); the gallery
site lives in `site/`. PR #28 (`chore/colab-runnable-notebooks`) awaits review/merge.

## Completed

- 2026-11-07: Added `notebooks/06_pyspark_coding_challenges.ipynb`: five interview-style PySpark problems
  (latest-record dedupe, grain-aware joins, SCD as-of join, sessionization, salted skew join) with fixtures, reference
  solutions and 19 asserts; runs locally in 13s. Recovered from the old WIP in `notebooks/04_pyspark_concepts.ipynb`.
- 2026-11-07: Verified PR #28: GitHub Checks green (all 57 notebooks executed on Linux + Java 17, 2m32s);
  smoke-tested in a real Google Colab runtime with "Run all": `topics/dynamodb` (30/30 cells), `topics/spark`
  (51/51, setup cell installed PySpark), `topics/iceberg` (22/22) — no errors.
- 2026-11-07: Colab-runnable restructure (`chore/colab-runnable-notebooks`):
  - Merged the open per-notebook cleanup PRs (#1–#22) and the notebook parts of #26 (DuckDB SQL) and #27
    (PySpark story); the interactive viewer (#24/#25) was intentionally dropped.
  - Moved the Next.js gallery into `site/`; upgraded Next.js to 16.4.5 (critical advisory on ≤16.4.0); fixed the
    Topics menu links ignoring the GitHub Pages base path.
  - Removed bloat: merged practice copies inside topics/python, sql, spark (~1,000 duplicated cells) and
    `sync_merged_copies.py`; the watermark tooling and per-notebook metadata (incl. email); the duplicate
    `topics/python-basics` and `topics/python-coding` notebooks (unique content folded into 01/02); committed
    outputs; "How to use" boilerplate; repeated prose (21,532 → 5,467 cells; many notebooks 40–80% fewer words).
  - Every `# ILLUSTRATIVE` cell became runnable code on an in-process stand-in or a markdown code fence.
  - Each notebook with third-party imports starts with a version-aware setup cell (`PACKAGES`), so Colab installs
    or upgrades exactly what it needs.
  - New tooling: `notebook_format.py`, Colab-rule `audit_notebooks.py`, parallel `run_notebooks.py`, pytest suite,
    ruff, Makefile `install/dev/test/lint/format/check/notebooks/build/validate`; CI runs every notebook with Java 17.
- 2026-10-17/18: Per-notebook dedupe sweep and DuckDB/PySpark rewrites (open PRs #1–#27, now folded in).

## In Progress

- Nothing.

## Next Steps

1. Review and merge PR #28 (https://github.com/sai-guntupalli/data-engineering-handbook/pull/28).
2. Close the superseded PRs #1–#27 (their content is in #28; #24/#25 viewer dropped by decision).
3. Reconcile the uncommitted exercise edits to `notebooks/04_pyspark_concepts.ipynb` in the main checkout
   (made against the old version) with the restructured notebook from #28.
4. Optional deeper trims: `04_pyspark_concepts` (12.9K words), `snowflake` (13.1K), `bigquery` (12.3K),
   `02_python_coding_problems` (12K).
5. Delete the stale local branches once #28 merges.

## Blockers

- None.
