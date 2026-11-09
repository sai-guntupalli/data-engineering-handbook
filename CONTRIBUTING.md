# Contributing

Notebooks are the product. A contribution is usually one `.ipynb` file under `notebooks/`.

## The rules every notebook follows

- **It runs in Google Colab.** "Runtime → Run all" in a fresh Colab runtime must finish without errors.
  CI executes every notebook to prove it.
- **Setup cell.** If a notebook imports anything outside the standard library, its first code cell installs it.
  Copy this shape and edit only `PACKAGES` (import name → pip spec). It also upgrades a preinstalled
  package that is too old (Colab ships its own versions):

  ```python
  # Setup: installs this notebook's packages when they are missing (e.g. in Google Colab).
  import importlib.util
  import subprocess
  import sys

  PACKAGES = {"duckdb": "duckdb>=1.0"}


  def _missing(module: str, spec: str) -> bool:
      """True when the module is absent or its installed version does not satisfy spec."""
      try:
          if importlib.util.find_spec(module) is None:
              return True
      except ModuleNotFoundError:
          return True
      try:
          from importlib.metadata import PackageNotFoundError, version

          from packaging.requirements import Requirement
      except ImportError:
          return False
      requirement = Requirement(spec)
      try:
          return not requirement.specifier.contains(version(requirement.name), prereleases=True)
      except PackageNotFoundError:
          return False


  missing = [spec for module, spec in PACKAGES.items() if _missing(module, spec)]
  if missing:
      subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", *missing])
  print("ready:", ", ".join(PACKAGES))
  ```

  Add the same packages to the `notebooks` extra in `pyproject.toml` so local runs and CI have them.
- **Colab-style installs.** A notebook may instead install a package with a plain `!pip install <package>` line,
  as the SQL path does for PySpark. The audit counts those packages as declared. Such a notebook still needs pip in
  the notebooks extra, which is already there.
- **No live systems.** Never connect to `localhost`, a cloud endpoint, or use credentials. Use in-process
  stand-ins: DuckDB for warehouse SQL, PySpark local mode, `deltalake`, `pyiceberg` (SQLite catalog), `fakeredis`,
  `mongomock`, `moto`, or a small pure-Python simulation.
- **Platform-only code goes in markdown.** YAML, shell, Scala, k8s manifests, or SQL dialects DuckDB cannot run
  belong in a fenced block in a markdown cell, not in a code cell.
- **Lean prose.** One `# Title` (first cell), then `##` sections and `###` subsections without skipping levels.
  One idea per markdown cell, a small runnable example below it, `assert`s that prove the point.
- **No committed outputs.** `make format` strips them and stamps the credit line and the Open in Colab badge.

## Workflow

```bash
make install     # uv sync --extra notebooks + site dependencies
make format      # canonical notebook form + ruff
make check       # audit every notebook (structure + Colab rules)
make notebooks   # execute every notebook (PySpark ones need Java 17+)
make validate    # everything CI runs
```

New notebooks go in the folder of the tool they teach, `notebooks/topics/<tool>/<slug>.ipynb`. Python notebooks sit in `learning/` or `practice/` inside it. A new tool needs a folder and an entry in
[`site/lib/tools.ts`](site/lib/tools.ts) so the gallery shows it. The build fails when a folder has no
entry or an entry has no folder.

## Commit checklist

- [ ] `make validate` passes.
- [ ] New packages are in both the notebook's `PACKAGES` and `pyproject.toml`.
- [ ] New notebooks are listed in `site/lib/notebook-groups.ts`.
- [ ] No secrets, tokens, personal data or machine-specific paths.

Contributions are published under the repository's [CC BY 4.0](LICENSE) license; by opening a pull request you
agree your contribution is licensed the same way.
