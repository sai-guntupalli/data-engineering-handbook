# Contributing

Notebooks are the product. A contribution is usually one `.ipynb` file under `notebooks/`.

## The rules every notebook follows

- **It runs in Google Colab.** "Runtime → Run all" in a fresh Colab runtime must finish without errors.
  CI executes every notebook to prove it.
- **Setup cell.** If a notebook imports anything outside the standard library, its first code cell installs it.
  Keep it to two lines: a `# Setup:` comment and one `!pip install` line. `pip` skips packages that are already
  satisfied and upgrades a preinstalled one that is too old (Colab ships its own versions):

  ```python
  # Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
  !pip install -q pyspark~=4.0.0 pyarrow
  ```

  Write each spec without quotes and without `<` or `>`: the line runs in a shell, where `>` redirects output,
  and the audit reads package names from the bare specs. Use `~=` for a version range (`pyspark~=4.0.0` means
  `>=4.0.0,<4.1`). Keep the `# Setup:` comment on the first line; `make verify-challenges` inserts its helpers right
  after that cell. Add the same packages to the `notebooks` extra in `pyproject.toml` so local runs and CI have
  them.

  Older notebooks use a longer setup cell that declares a `PACKAGES` mapping; the audit accepts both forms. Use the
  two-line form for new notebooks and when you rework an old one.
- **Short setup and sample data.** After the install line, start the session or connection and create the sample
  data in a cell or two. Create only the tables the notebook uses, and keep configuration to what the lessons need,
  with a comment on any setting that is not a default.
- **No live systems.** Never connect to `localhost`, a cloud endpoint, or use credentials. Use in-process
  stand-ins: DuckDB for warehouse SQL, PySpark local mode, `deltalake`, `pyiceberg` (SQLite catalog), `fakeredis`,
  `mongomock`, `moto`, or a small pure-Python simulation.
- **Platform-only code goes in markdown.** YAML, shell, Scala, k8s manifests, or SQL dialects DuckDB cannot run
  belong in a fenced block in a markdown cell, not in a code cell.
- **Lean prose.** One `# Title` (first cell), then `##` sections and `###` subsections without skipping levels.
  One idea per markdown cell, with a small runnable example below it.
- **Teach with output, not asserts.** An example shows its result: `print`, `.show()`, `explain()`, a table. A short
  `**What to notice:**` note after it says what the reader should see (the row that disappeared, the `Exchange` in
  the plan, the count that did not change) and why. Do not assert answers in learner-facing cells. Keep an `assert`
  only when checking is the lesson itself, such as a unit test or a pipeline's quality gate, and write that gate as
  a clear error (`raise ValueError(...)`) rather than a bare `assert` where you can. Maintainer checks belong in
  `tests/fixtures/`, as the challenge and practice checks below do. Because nothing asserts the numbers, check each
  note against a fresh run (`make outputs`) whenever you change an example.
- **Hidden solutions.** Practice problems give the statement, sample input and expected output first. The answer is a
  code cell tagged `solution` (Jupyter: *Cell → Cell Tags*, or `"tags": ["solution"]` in the cell metadata). The
  reader shows it closed; the formatter keeps the tag.
- **Difficulty.** Every practice problem and drill exercise has a line right under its heading:
  `**Difficulty:** Easy · about 5 min` (Easy, Medium or Hard, with an honest time estimate).
- **SQL/PySpark challenges.** Put the problem rules, readable sample input and complete expected output before the
  exercise and hidden solution. Keep grading assertions in `tests/fixtures/challenge-checks/`; preserve meaningful
  data-quality failure handling when it is part of the task. Run `make verify-challenges` to verify current answers
  against regression cases and the published output tables. Avoid scoreboards and test-only materialization code
  in the learner-facing notebook.
- **Checks that catch mistakes.** Keep Python practice checks in `tests/fixtures/practice-checks/`, outside the
  learner-facing notebook. Explain the question and show concrete sample inputs and expected outputs before the
  exercise cell. Avoid scoreboards and pass/todo output. Give each exercise 6-10 maintainer checks for empty input, single
  item, duplicates, ties, `None`, and the trap the exercise teaches. A check must be able to fail for a plausible wrong
  answer; confirm it against the reference solution and one deliberately wrong version with
  `uv run --extra notebooks python scripts/verify_practice_answers.py`.
- **Last reviewed.** Tool pages end their opening paragraph with `*Last reviewed: <Month YYYY>, against <tool and
  version>.*` (managed services: "against the <service> documentation as of <Month YYYY>"). Update it whenever you
  check the page against a new release, and confirm version-specific facts against official docs or release notes.
- **No committed outputs.** `make format` strips them and stamps the credit line and the Open in Colab badge. The
  site's results come from `make outputs`, which executes the notebooks into `build/executed` (git-ignored).

## Workflow

```bash
make install     # uv sync --extra notebooks + site dependencies
make format      # canonical notebook form + ruff
make check       # audit every notebook (structure + Colab rules)
make notebooks   # execute every notebook (PySpark ones need Java 17+)
make validate    # everything CI runs
```

New notebooks go in the folder of the tool they teach, `notebooks/topics/<tool>/<slug>.ipynb`. Python notebooks sit in `learning/` or `practice/` inside it. A new tool needs a folder and an entry in
[`site/lib/tools.ts`](site/lib/tools.ts), with a category from `TOOL_CATEGORIES`, so the gallery shows it. The build fails when a folder has no
entry or an entry has no folder.

### Naming notebooks

File names are lowercase kebab-case, with no underscores or leading numbers. A file name is also the page URL
(`/notebooks/<name>/`), so it must be unique across the repository. Start it with the tool folder name:

| Pattern | Use it for | Example |
| --- | --- | --- |
| `<tool>.ipynb` | a tool with one notebook | `kafka/kafka.ipynb` |
| `<tool>-<NN>-<subject>.ipynb` | an ordered series; `00` is an overview or start-here page | `sql/sql-01-basics.ipynb` |
| `<tool>-<series>-<NN>-<subject>.ipynb` | a numbered practice series | `python/practice/python-drills-01-values-and-types.ipynb` |
| `<tool>-<subject>.ipynb` | a standalone notebook | `sql/sql-reference.ipynb` |
| `<subject>.ipynb` | `concepts/` only, for subjects that are not a tool | `concepts/data-quality.ipynb` |

Titles use sentence case and keep product names as written (`Apache Kafka`, `dbt`). A numbered series uses
`<Series> <N>: <subject>`, for example `SQL 6: joins` or `Python drills 2: collections`. Words such as
`drills`, `challenges`, `practice`, `interview` and `reference` in a file name set its type on the tool page.

## Commit checklist

- [ ] `make validate` passes.
- [ ] New packages are in both the notebook's `PACKAGES` and `pyproject.toml`.
- [ ] New notebooks are listed in `site/lib/notebook-groups.ts`.
- [ ] No secrets, tokens, personal data or machine-specific paths.

Contributions are published under the repository's [CC BY 4.0](LICENSE) license; by opening a pull request you
agree your contribution is licensed the same way.
