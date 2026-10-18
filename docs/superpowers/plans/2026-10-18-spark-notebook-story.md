# PySpark Notebooks — Story Restructure Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/topics/spark` and the practice notebook `04_pyspark_concepts.ipynb` from dense one-cell-per-topic blocks into a narrative notebook: a clear story told in a meaningful order, one idea per cell, runnable examples carrying the explanation.

**Architecture:** Both notebooks keep their roles: the topic notebook is the reading experience (Parts 1–5 arc below — its authored first half), the practice notebook is the CI-executed exercise set whose merged self-contained copy lands in the topic notebook's tail region via `scripts/sync_merged_copies.py`. Restructure the practice notebook first, then the topic arc, then regenerate the merge so the two stay consistent.

**Spec decisions (user-confirmed 2026-10-18):** include the practice notebook; arc = Orientation → First session → Shaping data → Production patterns → Real world + interview; one idea per cell; keep everything runnable; merged region untouched by hand (regenerated via script).

## Global Constraints

- The **merged region** (from the merge-note cell to the notebook end, after cell ~245) is NEVER hand-edited — regenerate via the sync script after the practice restructure.
- Practice notebook must still execute green: `uv run --extra notebooks-spark python scripts/run_notebooks.py --check` (it IS one of the 5 CI-executed notebooks; 600 s/cell; PySpark + Java available).
- `make check` (audit), `make validate`, lint + site build must stay green; watermark/author metadata preserved (first credit line + `make watermark`).
- Every code cell stays runnable or is explicitly `# ILLUSTRATIVE` — the restructure must not convert runnable content into illustrative or vice versa (audit counts must reconcile: same runnable/illustrative totals ± new cells).
- Author metadata/watermark; markdown cells keep the repo's voice (second person, short, direct).
- Reading time in the card is computed from markdown words — a rewrite adds a little; keep total prose growth within ~15%.

## Review Focus

1. **Story continuity** — each Part opens with a short "why this comes now" connective cell; sections within a Part flow (no forward references before their concept is set).
2. **One idea per cell** — no markdown cell covers more than one concept; the 336-word intro and the 12-code-cell cookbook section are split into labeled mini-lessons (each with a heading or bold lead + its own runnable cell).
3. **Runnable integrity** — after restructure, every runnable cell still executes in a fresh kernel session; asserts preserved; order does not break statefulness (a cell using a variable defined earlier still comes after its definition).
4. **Sync consistency** — after both restructures, `sync_merged_copies.py --check` passes and the topic tail equals the practice content.
5. **No content loss** — every existing teaching unit survives (may move/split/retitled); the reviewer cross-checks the old section list (22 topic sections + practice structure) against the new one.

---

### Task 1: Restructure the practice notebook (04_pyspark_concepts.ipynb)

**Files:** modify `notebooks/04_pyspark_concepts.ipynb`. Produce: one-idea-per-cell, ordered basics→intermediate→production exercises, each concept cell (short prose) + runnable cell (assert-backed) pair; keep all existing asserts/techniques.

- [ ] **Step 1:** Restructure; run `uv run --extra notebooks-spark python scripts/run_notebooks.py --check` — Expected: green (all 5 practice notebooks).
- [ ] **Step 2:** Save outputs (`make notebooks`), then `make check` — Expected: green.
- [ ] **Step 3:** Commit `feat: restructure the pyspark practice notebook (one idea per cell)`.

### Task 2: Regenerate the merged region in topics/spark.ipynb

**Files:** modify `notebooks/topics/spark.ipynb` tail ONLY via `scripts/sync_merged_copies.py` merge mode.

- [ ] **Step 1:** Run sync (merge mode), then `scripts/sync_merged_copies.py --check` — Expected: green.
- [ ] **Step 2:** Commit `chore: regenerate the merged pyspark practice copy`.

### Task 3: Rebuild the topic-authored arc (cells 2..~245)

**Files:** modify `notebooks/topics/spark.ipynb` authored half only.

**The arc** (all existing teaching units preserved, reordered/split):
- **Part 1 — Orientation** (no code): 30-second pitch; where PySpark sits in a platform; RDDs vs DataFrames context (from the existing DataFrames section's explanatory cells); when you would NOT use PySpark. SPLIT the 336-word intro cell into ≤3 cells.
- **Part 2 — First session and the execution model**: SparkSession (+ a "predict output before running" note); read with explicit schemas; transformations vs actions; lazy evaluation (the payoff cell: nothing ran until an action); Spark SQL temp views; cleaning basics.
- **Part 3 — Shaping data**: joins (run the joining example); aggregations; window functions; the cookbook split into labeled mini-lessons (joins demo, pivot, dedupe, etc. — one runnable cell each with a bold lead); nested JSON/arrays.
- **Part 4 — Production patterns**: Unity Catalog writes; incremental pipeline; testing; bad records/DQ; UDFs; streaming; monitoring; performance (split its 379w/6-code block into labeled lessons).
- **Part 5 — Real world and interview**: use cases (split 478w/5-code); how to say it in an interview.
- Close by pointing into the merged practice region ("run the full worked examples below — they execute exactly the ideas above").

- [ ] **Step 1:** Rebuild the arc; keep every code cell runnable (verify no `# ILLUSTRATIVE` status flips — compare audit counts before/after).
- [ ] **Step 2:** `make check` — Expected: green; reading minutes not grown >~15%.
- [ ] **Step 3:** Interaction smoke (viewer, http://localhost:3000/topics/spark): run 2-3 cells live in the kernel (Part 2's session/data cells), zero errors.
- [ ] **Step 4:** Commit `feat: reorganize the spark topic notebook into a five-part story`.

### Task 4: Docs + full verification

**Files:** `PROGRESS.md` (dated entries), README only if counts/claims wrong.

- [ ] **Step 1:** `make validate` — Expected: all green (notebooks-check executes the restructured practice; lint + site build).
- [ ] **Step 2:** PROGRESS.md + commit `docs: pyspark story restructure notes`.