SHELL = /bin/bash

.PHONY: help up in down build bash

.DEFAULT_GOAL := help


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
