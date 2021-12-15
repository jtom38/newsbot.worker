.PHONY: help
help: ## Shows this help command
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Runs unit tests
	NEWSBOT_MODE='unittest'
	alembic upgrade head
	pytest

lint: ## Run flake8 against the project
	flake8 --ignore E501,F401,F405 ./workerApi

build: ## Build docker image
	docker build -t newsbot-worker:latest .

run: ## Runs the application
	docker-compose up

freeze: ## Exports all installed python packages to the requirements.txt
	pip3 freeze > requirements.txt
