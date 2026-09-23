.PHONY: install run format format-check lint lint-fix check clean

install:
	uv sync

run:
	uv run main.py

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

check: format-check lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
