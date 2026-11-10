# Data Engineering Handbook - common tasks.
#
#   make            # list targets
#   make validate   # everything CI runs

SHELL := /bin/bash
.DEFAULT_GOAL := help

PY   := uv run --extra notebooks python
# The formatter and audit are stdlib-only: no need to install notebook packages.
TOOL := uv run --no-project python
SITE := site
PORT ?= 3000
JOBS ?= 4
MOCKUPS := docs/mockups
MOCKUPS_PORT ?= 8000
# Executed notebook copies with outputs, read by the site build (see site/lib/notebooks.ts).
OUTPUTS ?= build/executed

.PHONY: help install dev test lint format check notebooks outputs build build-with-outputs mockups mockups-bundle validate stats clean

help: ## List available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install notebook packages, Python dev tools and site dependencies
	uv sync --extra notebooks
	npm --prefix $(SITE) ci

dev: ## Serve the gallery site locally (PORT=3000)
	npm --prefix $(SITE) run dev -- --port $(PORT)

test: ## Unit tests: notebook tooling (pytest) and the site's data layer (vitest)
	uv run pytest
	npm --prefix $(SITE) test

lint: ## Lint Python tooling and the site
	uv run ruff check scripts tests
	uv run ruff format --check scripts tests
	npm --prefix $(SITE) run lint

format: ## Format notebooks (credit, Colab badge, no outputs) and Python tooling
	$(TOOL) scripts/notebook_format.py
	uv run ruff format scripts tests
	uv run ruff check --fix scripts tests

check: ## Audit every notebook for Colab-runnability rules
	$(TOOL) scripts/notebook_format.py --check
	$(TOOL) scripts/audit_notebooks.py --quiet

notebooks: ## Execute every notebook top to bottom (JOBS=4); Spark ones need Java
	$(PY) scripts/run_notebooks.py --jobs $(JOBS)

outputs: ## Execute every notebook and save copies with trimmed outputs to build/executed
	$(PY) scripts/run_notebooks.py --jobs $(JOBS) --output-dir $(OUTPUTS)

build: ## Build the static gallery site (with the design mockups) into site/out
	npm --prefix $(SITE) run build
	$(MAKE) mockups-bundle

build-with-outputs: ## Execute the notebooks, then build the site showing their results
	-$(MAKE) outputs
	NOTEBOOK_OUTPUTS_DIR=$(OUTPUTS) $(MAKE) build

mockups: ## Serve the static design mockups locally (MOCKUPS_PORT=8000)
	python3 -m http.server $(MOCKUPS_PORT) --bind 127.0.0.1 --directory $(MOCKUPS)

mockups-bundle: ## Copy the design mockups into site/out/mockups for GitHub Pages
	rm -rf $(SITE)/out/mockups
	cp -R $(MOCKUPS) $(SITE)/out/mockups

validate: lint test check notebooks build ## Everything CI runs
	@echo "validate: all checks passed"

stats: ## Notebook counts and size
	@printf 'notebooks: %s\n' "$$(find notebooks -name '*.ipynb' | wc -l | tr -d ' ')"
	@printf 'size:      %s\n' "$$(du -sh notebooks | cut -f1)"

clean: ## Remove site build output and Python caches
	rm -rf $(SITE)/.next $(SITE)/out build .pytest_cache .ruff_cache
	find . -name '__pycache__' -type d -prune -not -path './.venv/*' -exec rm -rf {} +
