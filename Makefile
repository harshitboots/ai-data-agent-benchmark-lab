.PHONY: install dev test lint fmt clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check .

fmt:
	ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
