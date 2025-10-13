SHELL = /bin/bash

.PHONY: help up in down build bash freeze pytest cov env-file venv pre-commit setup

.DEFAULT_GOAL := help

VENV_DIR := .venv


help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'

up:  ## Start containers
	docker compose -f docker-compose.yaml up -d

in:  ## Open a bash shell in started cli service
	docker compose -f docker-compose.yaml exec -it cli bash

down:  ## Remove containers
	docker compose -f docker-compose.yaml down

build:  ## Build image
	docker compose -f docker-compose.yaml build

bash:  ## Open a bash shell in cli service
	docker compose -f docker-compose.yaml run --rm -it cli bash

freeze:  ## Run pip freeze (requirements.txt)
	pip freeze | grep -v "custom_cli" > requirements.txt

pytest:  ## Run pytest
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/code cli /bin/bash -c "python -m pytest"

cov:  ## Run tests and make coverage report
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app cli /bin/bash -c \
	"pytest --cov --cov-report html:coverage/html" \
	&& open coverage/html/index.html

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

setup: ## Setup environment, build images and containers, start cli
	@echo "🔧 Setting up environment..."
	@$(MAKE) env-file
	@$(MAKE) venv
	@$(MAKE) pre-commit
	@echo "🚀 Building Docker images and starting containers..."
	@$(MAKE) build
	@$(MAKE) up
	@echo "⚡ Containers started, opening bash shell..."
	docker compose -f docker-compose.yaml exec -it cli bash -c "echo '✅ Setup finished! Command to access the CLI: cli'; bash"
