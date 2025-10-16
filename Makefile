SHELL = /bin/bash

.PHONY: help up in down build log web-log pytest cov alembic-upgrade alembic-downgrade \
		bash freeze seed env-file venv pre-commit setup docs

.DEFAULT_GOAL := help

VENV_DIR := .venv


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'



# Docker
up:  ## Start containers
	docker compose -f docker-compose.yaml up -d

in:  ## Open a bash shell in started webapp service
	docker compose -f docker-compose.yaml exec -it webapp bash

down:  ## Remove containers
	docker compose -f docker-compose.yaml down

build:  ## Build image
	docker compose -f docker-compose.yaml build

log:  ## View logs
	docker compose logs -f

web-log:  ## View web logs
	docker compose logs webapp -f


# Tests
pytest:  ## Run pytest
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/code webapp /bin/bash -c "python -m pytest"

cov:  ## Run tests and make coverage report
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app webapp /bin/bash -c \
	"pytest --cov --cov-report html:coverage/html" \
	&& open coverage/html/index.html



# Alembic
alembic-upgrade:  ## Run alembic upgrades (development + production)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app webapp /bin/bash -c \
	"alembic upgrade head"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app webapp /bin/bash -c \
	"alembic upgrade head"

alembic-downgrade:  ## Run alembic downgrade -1 (development + production)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app webapp /bin/bash -c \
	"alembic downgrade -1"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app webapp /bin/bash -c \
	"alembic downgrade -1"



# Utils
bash:  ## Open a bash shell in webapp service
	docker compose -f docker-compose.yaml run --rm -it webapp bash

freeze:  ## Run pip freeze (requirements.txt)
	pip freeze | grep -v "custom_cli" > requirements.txt

seed: ## Seed database with users
	docker compose -f docker-compose.yaml run --rm -it webapp /bin/bash -c "cli seed"



# Env
env-file: ## Create an .env file based on .env.example
	@cp .env.example .env
	@echo "✅ Copied .env.example → .env"

venv: ## Create a Python virtual environment if not exists and install dependencies
	@echo "🐍 Creating Python virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
	fi
	@echo "📦 Installing dependencies from requirements.txt..."
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && pip install -e .
	@echo "✅ Virtual environment ready at $(VENV_DIR)"

pre-commit: ## Install and set up pre-commit hooks
	@echo "🧹 Installing pre-commit hooks..."
	@. $(VENV_DIR)/bin/activate && pip install pre-commit && pre-commit install
	@echo "✅ Pre-commit hooks installed"

setup: ## Setup environment, build images and containers, start webapp
	@echo "🔧 Setting up environment..."
	@$(MAKE) env-file
	@$(MAKE) venv
	@$(MAKE) pre-commit
	@echo "🚀 Building Docker images and starting containers..."
	@$(MAKE) build
	@$(MAKE) up
	@echo "Waiting for PostgreSQL to be ready..."
		@until docker compose -f docker-compose.yaml exec -T db-development sh -c 'pg_isready -U postgres -d db-development | grep "accepting connections" > /dev/null'; do \
			echo "Still waiting..."; \
			sleep 1; \
		done
	sleep 5
	@$(MAKE) alembic-upgrade
	@$(MAKE) seed
	@echo "⚡ Containers started, opening docs..."
	@$(MAKE) docs

docs: ## Open Swagger UI
	@python -c "import webbrowser; webbrowser.open('http://localhost:8000/docs')"
