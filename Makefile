# Data Engineering Interview Notebooks - common tasks.
#
#   make            # list targets
#   make validate   # notebook audit + execution + app build

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Prefer the repository virtualenv, then uv's pinned interpreter; bare `python3`
# is a last resort that may predate the notebooks' 3.12 requirement.
PY  ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; elif command -v uv >/dev/null 2>&1; then echo "uv run python"; else echo python3; fi)
NPM ?= npm

PORT ?= 3000

.PHONY: help setup setup-notebooks setup-spark chat-install check watermark notebooks notebooks-check notebook-audit sync-check site lint serve dev-local test validate stats clean

help: ## List available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-17s\033[0m %s\n", $$1, $$2}'

setup: ## Install Python tooling and app dependencies
	uv sync
	$(NPM) install

setup-notebooks: ## Install notebook tooling (nbformat, nbclient, ipykernel)
	uv sync --extra notebooks

setup-spark: ## Install notebook tooling plus PySpark and pandas (requires Java 17+)
	uv sync --extra notebooks --extra notebooks-spark

chat-install: ## Install interactive-viewer backend tooling (fastapi, uvicorn, httpx, pytest-httpx)
	uv sync --extra interactive

check: ## Validate every notebook (format, metadata, non-empty cells)
	$(PY) scripts/audit_notebooks.py --quiet

watermark: ## Stamp the author watermark (metadata + credit line) into all notebooks
	$(PY) scripts/watermark_notebooks.py

notebooks: ## Execute the practice notebooks and save their outputs
	$(PY) scripts/run_notebooks.py

notebooks-check: ## Execute the practice notebooks without writing outputs (CI-safe)
	$(PY) scripts/run_notebooks.py --check

notebook-audit: ## Print a notebook inventory with cell counts
	$(PY) scripts/audit_notebooks.py

sync-check: ## Verify merged copies match their practice notebooks
	$(PY) scripts/sync_merged_copies.py --check

site: ## Build the notebook gallery app
	$(NPM) run build

lint: ## Lint the gallery app
	$(NPM) run lint

serve: ## Serve the gallery locally (PORT=3000 by default)
	$(NPM) run dev -- --port $(PORT)

dev-local: ## Run the chat backend (127.0.0.1:8077) and the gallery dev server together
	PORT=$(PORT) ./scripts/dev-local.sh

test: ## Run gallery unit tests and the chat backend tests
	$(NPM) test
	# All three extras are named explicitly: `uv run` prunes any extra not listed,
	# so this must not strip the notebook tooling `make validate` needs from the venv.
	uv run --extra notebooks --extra notebooks-spark --extra interactive pytest backend/tests -q

validate: check sync-check notebooks-check lint site ## Full pipeline: notebook audit + sync + execution + app lint + build
	@echo "validate: all checks passed"

stats: ## Show notebook counts and size
	@printf 'notebooks: %s\n' "$$(find notebooks -name '*.ipynb' | wc -l | tr -d ' ')"
	@printf 'practice:  %s\n' "$$(ls notebooks/*.ipynb | wc -l | tr -d ' ')"
	@printf 'topics:    %s\n' "$$(ls notebooks/topics/*.ipynb | wc -l | tr -d ' ')"
	@printf 'size:      %s\n' "$$(du -sh notebooks | cut -f1)"

clean: ## Remove app build output and Python caches
	rm -rf .next out
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	@echo "cleaned build output and __pycache__ directories"
