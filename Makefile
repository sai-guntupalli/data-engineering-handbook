# Data Engineering Interview Guide - common local tasks.
#
#   make            # list targets
#   make validate   # strict checks + index sync + strict site build
#
# Tool overrides, e.g.:
#   make site MKDOCS="uv run mkdocs"
#   make serve PORT=8001

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Prefer the repository virtualenv when it exists; otherwise fall back to uv/system tools.
PY        ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
MKDOCS    ?= $(shell if [ -x .venv/bin/mkdocs ]; then echo .venv/bin/mkdocs; else echo "uv run mkdocs"; fi)
DOCS_PREP ?= $(shell if [ -x .venv/bin/python ]; then echo ".venv/bin/python scripts/build_docs_source.py"; else echo "uv run docs-prepare"; fi)

PORT ?= 8000

.PHONY: help setup setup-notebooks setup-spark check check-strict full full-check docs nav-check site serve notebooks notebooks-check topic-notebooks topic-notebooks-check notebook-links notebook-links-check validate ci stats clean

help: ## List available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies with uv (creates .venv)
	uv sync

check: ## Run repository checks (links, encoding, placeholders)
	$(PY) scripts/repo_checks.py

check-strict: ## Repository checks plus anchor validation against content/full.md
	STRICT_ANCHORS=1 $(PY) scripts/repo_checks.py

full: ## Regenerate content/full.md from the headings in content/*.md
	$(PY) scripts/generate_full.py > content/full.md
	@printf 'content/full.md regenerated: %s lines\n' "$$(wc -l < content/full.md)"

full-check: ## Verify content/full.md is in sync without writing (CI-safe)
	@$(PY) scripts/generate_full.py | diff -u content/full.md - && echo "content/full.md is in sync"

docs: ## Generate the MkDocs source tree in .docs_src
	$(DOCS_PREP)

nav-check: ## Fail when a topic is missing from the mkdocs.yml navigation
	$(PY) scripts/build_docs_source.py --strict-nav

site: docs ## Build the static site with strict warnings enabled
	$(MKDOCS) build --strict

serve: docs ## Serve the docs locally (PORT=8000 by default)
	$(MKDOCS) serve -a 127.0.0.1:$(PORT)

setup-notebooks: ## Install notebook tooling (jupyter, nbclient, ipykernel)
	uv sync --extra notebooks

setup-spark: ## Install notebook tooling plus PySpark and pandas (requires Java 17+)
	uv sync --extra notebooks --extra notebooks-spark

notebooks: ## Execute every notebook in notebooks/ and save their outputs
	$(PY) scripts/run_notebooks.py

notebooks-check: ## Execute notebooks without writing outputs (CI-safe)
	$(PY) scripts/run_notebooks.py --check

topic-notebooks: ## Regenerate notebooks/topics/*.ipynb from content/*.md
	$(PY) scripts/md_to_notebooks.py

topic-notebooks-check: ## Verify notebooks/topics/*.ipynb are up to date (CI-safe)
	$(PY) scripts/md_to_notebooks.py --check

notebook-links: ## Add or refresh the notebook link at the top of every topic document
	$(PY) scripts/link_notebooks.py

notebook-links-check: ## Fail when a topic document is missing its notebook link (CI-safe)
	$(PY) scripts/link_notebooks.py --check

validate: check-strict full-check nav-check notebook-links-check site ## Full pipeline: strict checks + index sync + nav/link coverage + strict build
	@echo "validate: all checks passed"

ci: validate ## Alias for validate

stats: ## Show document, question, code-block and line counts
	@printf 'docs:        %s\n' "$$(ls content/*.md | grep -vc 'full.md')"
	@printf 'questions:   %s\n' "$$(ls content/*.md | grep -v 'full.md' | xargs grep -h '^## ' | grep -vc '\[Main title\]')"
	@printf 'code blocks: %s\n' "$$(ls content/*.md | grep -v 'full.md' | xargs grep -h '^```' | wc -l | awk '{print int($$1/2)}')"
	@printf 'lines:       %s\n' "$$(ls content/*.md | grep -v 'full.md' | xargs cat | wc -l)"

clean: ## Remove generated site, docs source and Python caches
	rm -rf site .docs_src
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	@echo "cleaned site/, .docs_src/ and __pycache__ directories"
