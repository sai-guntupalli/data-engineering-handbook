# Contributing

Notebooks are the source of truth in this repository. There is no Markdown content pipeline to keep in sync, so a
contribution is usually just one `.ipynb` file.

## Quick checks

```bash
make setup            # Python tooling + app dependencies
make check            # notebook structure audit
make notebooks-check  # execute the practice notebooks
make validate         # audit + execution + gallery build
```

`make validate` is what CI runs.

## Adding or changing a topic notebook

1. Create `notebooks/topics/<topic>.ipynb` (or edit an existing one).
2. Register the slug in the right group in [`lib/notebook-groups.ts`](lib/notebook-groups.ts) so it appears in the
   gallery.
3. Run `make check` (structure) and, if it is a practice notebook, `make notebooks-check` (execution).

Practice notebooks live at `notebooks/01..05_*.ipynb`; they are executed by CI, so keep them deterministic, standard
library only, and fast.

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

## Commit checklist

- [ ] `make validate` passes.
- [ ] The notebook has no error outputs and runs top to bottom.
- [ ] New notebooks are listed in `lib/notebook-groups.ts`.
- [ ] No secrets, tokens, personal data or machine-specific paths.
