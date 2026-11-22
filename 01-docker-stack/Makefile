COMPOSE = docker compose -f compose.yaml

.PHONY: up down logs backup restore

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

backup:
	$(COMPOSE) exec -T db pg_dump -U app appdb > backups/appdb.sql

restore:
	$(COMPOSE) exec -T db psql -U app appdb < backups/appdb.sql
