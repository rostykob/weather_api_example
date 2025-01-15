.PHONY: help install test lint run build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make build     - Build Docker image"
	@echo "  make drun - Run the application in Docker"
	@echo "  make clean     - Clean up generated files"

install:
	pip install -r requirements.txt

build:
	./scripts/docker-build.sh

drun:
	docker compose up -d
ddown:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete