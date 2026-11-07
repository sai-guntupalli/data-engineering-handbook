# Progress

**Current Status**: All 57 notebooks are Colab-runnable, lean, and executed by CI; the gallery site lives in
`site/`. The restructure is on `chore/colab-runnable-notebooks`, awaiting review/merge.

## Completed

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

1. Review and merge the `chore/colab-runnable-notebooks` PR; confirm the Checks workflow passes on GitHub
   (first CI run of all 57 notebooks with Java 17 on Linux).
2. Close the superseded PRs #1–#27 (their content is in this PR; #24/#25 viewer dropped by decision).
3. Smoke-test a few notebooks in a real Colab runtime (one Spark: `topics/spark.ipynb`; one Iceberg:
   `topics/iceberg.ipynb`; one moto: `topics/dynamodb.ipynb`) to confirm Colab's preinstalled versions + setup cell.
4. Optional deeper trims: `04_pyspark_concepts` (12.9K words), `snowflake` (13.1K), `bigquery` (12.3K),
   `02_python_coding_problems` (12K).
5. Delete the stale local branches once the PR merges.

## Blockers

- None.
