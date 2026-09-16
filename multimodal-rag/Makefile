.PHONY: help install run test clean lint format

help:
	@echo "Multimodal RAG - Make Commands"
	@echo "==============================="
	@echo "install    - Install dependencies"
	@echo "run        - Run the FastAPI server"
	@echo "test       - Run tests"
	@echo "lint       - Run linting"
	@echo "format     - Format code"
	@echo "clean      - Clean generated files"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

test:
	pytest tests/ -v --cov=app

lint:
	ruff check app/

format:
	black app/ tests/
	ruff check --fix app/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
