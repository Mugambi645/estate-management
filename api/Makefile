# Makefile — Docker Compose helpers for estate_prod

.DEFAULT_GOAL := help
.PHONY: help build up down down-v show-logs show-logs-api \
        makemigrations migrate collectstatic superuser \
        db-volume mailpit-volume estate-db

COMPOSE := docker compose -f local.yml
PROJECT_APPS := issues users common profiles ratings post

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build:  ## Rebuild images and start the stack detached
	$(COMPOSE) up --build -d --remove-orphans

up:  ## Start the stack detached
	$(COMPOSE) up -d

down:  ## Stop the stack
	$(COMPOSE) down

down-v:  ## Stop the stack and remove volumes
	$(COMPOSE) down -v

show-logs:  ## Tail all logs
	$(COMPOSE) logs -f

show-logs-api:  ## Tail API logs
	$(COMPOSE) logs -f api

makemigrations:  ## Generate migrations for project apps only
	$(COMPOSE) run --rm api python manage.py makemigrations $(PROJECT_APPS)

migrate:  ## Apply Django migrations
	$(COMPOSE) run --rm api python manage.py migrate

collectstatic:  ## Collect static files
	$(COMPOSE) run --rm api python manage.py collectstatic --no-input --clear

superuser:  ## Create a Django superuser
	$(COMPOSE) run --rm api python manage.py createsuperuser

db-volume:  ## Inspect the Postgres volume
	docker volume inspect api_estate_prod_postgres_data

mailpit-volume:  ## Inspect the Mailpit volume
	docker volume inspect api_estate_prod_mailpit_data

estate-db:  ## Open a psql shell in the Postgres container
	$(COMPOSE) exec postgres psql --username=patrickmugambi --dbname=estate	/staticfiles/*
	!/staticfiles/.gitkeep