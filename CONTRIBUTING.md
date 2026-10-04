## Contributing

Contributions are welcome: new questions, fixes, better links, and formatting improvements.

### Quick checks

Run the full local pipeline before opening a PR:

```bash
make validate
```

That runs the strict repository checks (anchor validation included), verifies `content/full.md` is in sync, and builds the site with warnings treated as errors. Individual targets:

```bash
make check          # repository checks (links, encoding, placeholders)
make check-strict   # same, plus anchors validated against content/full.md
make full           # regenerate content/full.md after adding or renaming headings
make full-check     # verify content/full.md is in sync without writing
make site           # mkdocs build --strict
make serve          # local preview at http://127.0.0.1:8000 (PORT=8001 to change)
make stats          # document, question, code-block and line counts
make clean          # remove site/, .docs_src/ and __pycache__ directories
```

Without `make`, the underlying commands are:

```bash
python3 scripts/repo_checks.py
STRICT_ANCHORS=1 python3 scripts/repo_checks.py
python3 scripts/generate_full.py > content/full.md
uv run mkdocs build --strict
```

### Content guidelines

- Keep files **UTF-8** encoded.
- Avoid placeholder links like `TODO` in markdown or HTML.
- If you add links in `content/full.md`, make sure the referenced heading exists in the target file.
- Every topic file starts with `## [Main title](../README.md)`, `### [Interview questions](full.md)`, a blank line, then `# <Title>` and a hand-written question TOC.
- When adding a new topic file, register its slug in `scripts/build_docs_source.py` (`TOPIC_GROUPS`), add a row to the README table, then run `make full` and `make validate`.

