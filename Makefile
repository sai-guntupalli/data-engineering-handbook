# Data Engineering Interview Notebooks - common tasks.
#
#   make            # list targets
#   make validate   # notebook audit + execution + app build

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Prefer the repository virtualenv when it exists; otherwise fall back to system tools.
PY  ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
NPM ?= npm

PORT ?= 3000

.PHONY: help setup setup-notebooks setup-spark check notebooks notebooks-check notebook-audit site serve validate stats clean

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

check: ## Validate every notebook (format, metadata, non-empty cells)
	$(PY) scripts/audit_notebooks.py --quiet

notebooks: ## Execute the practice notebooks and save their outputs
	$(PY) scripts/run_notebooks.py

notebooks-check: ## Execute the practice notebooks without writing outputs (CI-safe)
	$(PY) scripts/run_notebooks.py --check

notebook-audit: ## Print a notebook inventory with cell counts
	$(PY) scripts/audit_notebooks.py

site: ## Build the notebook gallery app
	$(NPM) run build

serve: ## Serve the gallery locally (PORT=3000 by default)
	$(NPM) run dev -- --port $(PORT)

validate: check notebooks-check site ## Full pipeline: notebook audit + execution + app build
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
