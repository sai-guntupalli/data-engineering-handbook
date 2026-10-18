# SQL Notebook → DuckDB Deep Rewrite Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `notebooks/03_sql_interview_questions.ipynb` as the DuckDB-powered SQL interview notebook and let every cell run interactively in the new local viewer; the merged `notebooks/topics/sql.ipynb` copy follows automatically via `scripts/sync_merged_copies.py`.

**Architecture:** The notebook keeps its proven shape — in-memory database + `run()`/`show()` helpers + asserts-as-self-checks — but the engine becomes DuckDB (`duckdb.connect(":memory:")`), which unlocks analytics SQL SQLite could not express (QUALIFY, PIVOT/UNPIVOT, ASOF joins, LIST/STRUCT types, richer EXPLAIN). The interactive viewer (PR #25) executes cells through the persistent kernel, so "make it interactive" is achieved by the notebook being genuinely runnable + the venv carrying duckdb.

**Tech Stack:** DuckDB (pyproject `notebooks` extra), existing notebook conventions (watermark metadata, `### Try it` blocks, assert-counted self-checks), `scripts/audit_notebooks.py`, `scripts/run_notebooks.py`, `scripts/sync_merged_copies.py`, `make validate`.

**Spec decisions (user-confirmed 2026-10-18):** deep rewrite (port + refresh + DuckDB-specific skills); stacked branch `feat/sql-duckdb` off `feat/interactive-notebook-viewer`; `duckdb` in the `notebooks` extra.

## Global Constraints

- Engine is DuckDB only — no sqlite remnants in code cells or markdown claims.
- The notebook MUST execute end-to-end in a fresh venv with the `notebooks` extra: `uv run --extra notebooks python scripts/run_notebooks.py --check` (600 s ceiling per cell).
- Every runnable claim keeps at least one `assert` (self-check discipline, matches repo stats which count `\bassert\b`).
- Keep the watermark/author metadata block exactly (first markdown cell credit line + notebook metadata; `make watermark` re-stamps).
- `scripts/sync_merged_copies.py --check` and `scripts/audit_notebooks.py` must pass; the merged topics/sql.ipynb must regenerate via that script, never hand-edited.
- `make validate` (audit + sync-check + notebooks-check + lint + site build) must pass at the end.
- Reading-time/claims in markdown must not exaggerate: update the intro's "how to use this notebook" wording to DuckDB.
- pyproject single source of truth: add `duckdb>=1.0` to the `notebooks` extra (and `uv lock`). README's dependency mentions updated only where wrong.

## Review Focus

1. **Fetchall type drift.** DuckDB returns Python-native types (DECIMAL as decimal.Decimal, DATE objects, floats). Every assert that compares exact values/types must pass under DuckDB — no assert may pass only under SQLite semantics. Test: the notebook executes green via `run_notebooks.py --check`.
2. **Markdown-code drift.** Markdown must describe what the code does in DUCKDB (e.g., median via `median()`/`quantile_cont`, EXPLAIN output shapes). Any sentence that says "SQLite" in an explanatory claim is a finding.
3. **Lost pedagogy.** All 22 Q's and 14 T's must remain — renumbering/regrouping allowed, dropping content is not (the T-section interview cards are the point of the notebook).
4. **New DuckDB sections must be runnable, not illustrative.** QUALIFY/PIVOT/ASOF etc. need no external platform — they must be plain runnable cells with asserts (never `# ILLUSTRATIVE`).
5. **Interaction smoke.** In the viewer (practice notebook page), the setup cell + at least one Q-cell run live in the browser kernel without error.

---

### Task 1: Dependency + helper-layer foundation

**Files:**
- Modify: `pyproject.toml` (`notebooks` extra gets `duckdb>=1.0`), `uv.lock` (via `uv lock`)
- Modify: `README.md` only if a dependency list names the notebooks extra and is now wrong
- Modify: `notebooks/03_sql_interview_questions.ipynb` (setup section only)

**Interfaces:**
- Produces: in-notebook API used by ALL later cells —
  `conn = duckdb.connect(":memory:")`, `run(sql, params=())` (execute, returns list of tuples), `show(sql, params=(), max_rows=30)` (prints a small table; MUST NOT require pandas — format from DuckDB's own result, e.g. `.arrow()`/fetch + hand-rolled column widths). Names/signatures unchanged from the current notebook so downstream cells keep working.

- [ ] **Step 1:** Add `duckdb>=1.0` to the `notebooks` extra; `uv lock` (lockfile update included in this task's commit).
- [ ] **Step 2:** Run `uv sync --extra notebooks` then `uv run --extra notebooks python -c "import duckdb; print(duckdb.__version__)"` — Expected: a version prints, no error.
- [ ] **Step 3:** Rewrite ONLY the setup section (through "Row-count sanity check" + structural invariants) of the practice notebook: in-memory DuckDB, `run`/`show` helpers (asserted), duckdb version print, the same six-seed-table DDL with DuckDB-native types, with asserts proving helpers + row counts. Keep the watermark/author first cell intact.
- [ ] **Step 4:** Execute the notebook (nbclient or the run script; save outputs in place with run_notebooks.py non-check mode) — Expected: zero failures; helper asserts green.
- [ ] **Step 5:** Commit `feat: duckdb engine and setup helpers for the sql notebook`.

### Task 2: Port Q1–Q22 to DuckDB + dialect fixes

**Files:**
- Modify: `notebooks/03_sql_interview_questions.ipynb`

**Interfaces:**
- Consumes: `run`/`show`/`conn` from Task 1.
- Produces: 22 interview questions each with explanation markdown, runnable `show(...)`/`run(...)` cells, and ≥1 assert; DuckDB-idiomatic answers (window filters via `QUALIFY` where clearer; Q17 pivot gains real `PIVOT`/`UNPIVOT` alongside CASE; Q18 median via `median()`/`quantile_cont`; Q5 delete-duplicates keeps DuckDB-valid in-place logic; Q2 nth-highest may use OFFSET/window).

- [ ] **Step 1:** Port cells Q1–Q22 (content preserved; dialect updated; every assert passes under DuckDB; fix fetchall-type drift).
- [ ] **Step 2:** Run `uv run --extra notebooks python scripts/run_notebooks.py --check` — Expected: notebook executes green, all asserts pass.
- [ ] **Step 3:** Commit `feat: port sql questions to duckdb semantics`.

### Task 3: DuckDB-specific section + theory refresh

**Files:**
- Modify: `notebooks/03_sql_interview_questions.ipynb`

**Interfaces:**
- Consumes: seed tables from Task 1.
- Produces: a new `## DuckDB skills that SQLite could not teach` section with ~5 runnable lessons: (1) `QUALIFY` (rewrite a window filter), (2) `PIVOT`/`UNPIVOT` (real syntax), (3) `ASOF JOIN` (point-in-time latest lookup — may need one extra seed table: prices per day), (4) LIST + STRUCT types (aggregate into typed nested values; query them), (5) `EXPLAIN`/`EXPLAIN ANALYZE` reading (refresh T2's plan-reading card to DuckDB shapes: HASH_JOIN, SEQ_SCAN, etc.). T1–T14 stay; wording refreshed only where SQLite mechanics were referenced.

- [ ] **Step 1:** Write the new section's cells with asserts.
- [ ] **Step 2:** Notebook executes green (`run_notebooks.py --check`).
- [ ] **Step 3:** Commit `feat: duckdb-specific lessons (qualify, pivot, asof, structs, explain)`.

### Task 4: Merge copy, metadata, docs, interaction smoke

**Files:**
- Modify: `notebooks/topics/sql.ipynb` (VIA `scripts/sync_merged_copies.py` only — regenerate, never hand-edit)
- Modify: `README.md` / `PROGRESS.md` if warranted
- Test: `make validate`

**Interfaces:**
- Consumes: rewritten practice notebook.

- [ ] **Step 1:** `make watermark` (re-stamp metadata), then `make check` (audit) — Expected: pass.
- [ ] **Step 2:** `scripts/sync_merged_copies.py --check`, then merge mode — Expected: topics/sql.ipynb regenerates with the new DuckDB cells.
- [ ] **Step 3:** `make validate` (full loop: audit + sync-check + notebooks-check + lint + site build) — Expected: all green.
- [ ] **Step 4:** Interaction smoke: with `make dev-local` running (it is already up in this worktree), open the practice notebook's viewer page and Run the setup cell + one Q-cell in the browser — Expected: DuckDB outputs render.
- [ ] **Step 5:** Commit `feat: merged topic copy and docs for the duckdb sql notebook`.