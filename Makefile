# Makefile - BlobLite Dev Toolkit

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help setup run test lint format clean upgrade-deps build publish check freeze test-cli

help:
	@echo "🔧 BlobLite - Dev Commands:"
	@echo "  setup         → Create venv only"
	@echo "  install       → Install all dev dependencies"
	@echo "  run           → Run example safely"
	@echo "  test          → Run all tests with pytest"
	@echo "  test-cli      → Run only CLI tests"
	@echo "  lint          → Lint code with ruff"
	@echo "  format        → Format code with black"
	@echo "  clean         → Remove __pycache__ and .pyc files"
	@echo "  build         → Build the distribution packages"
	@echo "  publish       → Upload to PyPI"
	@echo "  upgrade-deps  → Upgrade pip and dev dependencies"
	@echo "  check         → Lint, test, and build"
	@echo "  freeze        → Save exact dependency versions"

setup:
	@echo "📦 Setting up virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "✅ Virtual environment created."
	@echo "👉 Run 'source $(VENV_DIR)/bin/activate' to activate it."

install:
	@echo "📥 Installing dev dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements-dev.txt
	@echo "✅ Dependencies installed."

run:
	@echo "🚀 Running example..."
	@$(PYTHON) examples/main.py

test:
	@echo "🧪 Running tests..."
	@$(PYTHON) -m pytest tests

test-cli:
	@echo "🧪 Testing CLI interface..."
	@$(PYTHON) -m pytest tests/test_cli.py

lint:
	@echo "🔍 Linting with ruff..."
	@$(VENV_DIR)/bin/ruff check src tests examples

format:
	@echo "🧼 Formatting code with black..."
	@$(VENV_DIR)/bin/black src tests examples

clean:
	clear
	@echo "🧹 Cleaning cache..."
	@find . -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null
	@find . -type d -name '.pytest_cache' -exec rm -r {} + 2>/dev/null
	@find . -type f -name '*.pyc' -delete 2>/dev/null
	@echo "✅ Clean complete."

upgrade-deps:
	@echo "⬆️  Upgrading all dependencies..."
	@$(PIP) install --upgrade pip setuptools wheel >/dev/null
	@$(PIP) install --upgrade -r requirements-dev.txt >/dev/null
	@echo "✅ Dependencies upgraded."

build:
	@echo "📦 Building package..."
	@$(PYTHON) -m build

publish:
	@echo "🚀 Publishing to PyPI..."
	@$(PYTHON) -m twine upload dist/*

check:
	@echo ""
	@echo "========================= 🧪 BLOBLITE CHECK ========================="
	@echo "🔍 1. Linting with ruff..."
	@$(MAKE) lint || (echo '❌ Lint failed' && exit 1)

	@echo ""
	@echo "🧪 2. Running tests with pytest..."
	@$(MAKE) test || (echo '❌ Tests failed' && exit 1)

	@echo ""
	@echo "📦 3. Building package..."
	@$(PYTHON) -m build > /dev/null || (echo '❌ Build failed' && exit 1)

	@echo ""
	@echo "✅ All checks passed successfully!"
	@echo "===================================================================="

freeze:
	@echo "📄 Freezing current environment..."
	@$(PIP) freeze > requirements-lock.txt
