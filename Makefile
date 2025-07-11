# Makefile - Clean Developer Experience

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help setup run test lint format clean

help:
	@echo "🔧 BlobLite - Dev Commands:"
	@echo "  setup    → Create venv and install dependencies"
	@echo "  run      → Run example safely"
	@echo "  test     → Run tests with pytest"
	@echo "  lint     → Lint code with flake8"
	@echo "  format   → Format code with black"
	@echo "  clean    → Remove cache files"

setup:
	@echo "📦 Setting up virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install -e . >/dev/null
	@$(PIP) install -r requirements-dev.txt >/dev/null
	@echo "✅ Setup complete."

run:
	@echo "🚀 Running example..."
	@$(PYTHON) examples/main.py

test:
	@echo "🧪 Running tests..."
	@$(PYTHON) -m pytest tests

lint:
	@echo "🔍 Linting..."
	@$(VENV_DIR)/bin/flake8 bloblite examples tests

format:
	@echo "🧼 Formatting code..."
	@$(VENV_DIR)/bin/black bloblite examples tests

clean:
	@echo "🧹 Cleaning cache..."
	@find . -type d -name '__pycache__' -exec rm -r {} + 2>/dev/null
	@find . -type f -name '*.pyc' -delete 2>/dev/null
	@echo "✅ Clean complete."
