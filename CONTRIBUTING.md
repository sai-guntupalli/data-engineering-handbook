# Contributing

Notebooks are the source of truth in this repository. There is no Markdown content pipeline to keep in sync, so a
contribution is usually just one `.ipynb` file.

## Quick checks

```bash
make setup            # Python tooling + app dependencies
make check            # notebook structure audit
make notebooks-check  # execute the practice notebooks
make sync-check       # merged Colab copies match their practice notebooks
make lint             # lint the gallery app
make validate         # audit + sync + execution + app lint + gallery build
```

`make validate` is what CI runs.

## Adding or changing a topic notebook

1. Create `notebooks/topics/<topic>.ipynb` (or edit an existing one).
2. Register the slug in the right group in [`lib/notebook-groups.ts`](lib/notebook-groups.ts) so it appears in the
   gallery.
3. Run `make check` (structure) and, if it is a practice notebook, `make notebooks-check` (execution).

Practice notebooks live at `notebooks/01..05_*.ipynb`; they are executed by CI, so keep them deterministic, standard
library only, and fast.

## Merged copies

`topics/python.ipynb`, `topics/spark.ipynb` and `topics/sql.ipynb` end with a copy of a practice notebook so each topic
reads and runs as one self-contained notebook. After editing `01`–`04`, refresh the copies so they keep reading and
running like the source:

```bash
make notebooks                                    # execute the practice notebooks and save outputs
uv run python scripts/sync_colab_merges.py        # refresh the merged copies (copies code + outputs)
make validate
```

CI runs `make sync-check` and fails when a merged copy drifted from its source.

## Notebook style

The goal is that a reader who has never seen the topic can follow it from the top.

- Start with a `# Title` markdown cell and a short intro saying what the notebook covers and how to run it.
- Explain one idea per markdown cell in plain language, then put a **small** code cell right below it.
- Keep code cells short (roughly 3-12 lines). Do not mix unrelated ideas in one cell or one section.
- Make examples print something, so the reader sees the result when running the cell.
- Follow explanations with `### Try it` exercises: task, hint, expected result.
- Use `assert` in practice notebooks so the reader (and CI) can verify the answer.
- Prefer the standard library. Guard optional runtimes (PySpark, databases) behind an availability check and print a
  helpful message instead of failing.
- Use plain, concrete language and short sentences; define a term the first time it appears.
- Every runnable demo must be self-contained: create fixture files inline (`io.StringIO`, `tempfile`) instead of
  reading from disk, and never reference files outside the notebook.
- Cells that need a platform (Spark, Kafka, a cloud SDK) must not break the run: either guard them with
  `try`/`except ModuleNotFoundError` printing a `SKIPPED` message, or mark them with a first-line
  `# ILLUSTRATIVE - requires <deps>: install to run, or read on.` comment.

## Commit checklist

- [ ] `make validate` passes.
- [ ] The notebook has no error outputs and runs top to bottom.
- [ ] New notebooks are listed in `lib/notebook-groups.ts`.
- [ ] No secrets, tokens, personal data or machine-specific paths.
