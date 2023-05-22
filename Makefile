fresh_run: down
	docker compose build
	docker compose up

down:
	docker compose down --remove-orphans

restore_demo:
	docker exec -i sql-diploma-db_demo-1 psql -f demo_small.sql -U postgres

build_demo:
	docker build . -f demo.dockerfile -t 'sql-diploma-db_demo'


## migration: create alembic migration with revision name in {num_by_day}_{revision_comment} format
migration:
	@read -p "Enter revision name in {num_by_day}_{revision_comment} format: " revision_name; \
	docker compose run app alembic revision --autogenerate -m $$revision_name

## upgrade:   upgrade alembic migrations
upgrade:
	docker compose run app alembic upgrade head

## downgrade: downgrade alembic migrations
downgrade:
	docker compose run app alembic downgrade base


## pip-compile: compile all requirements
pip-compile:
	docker compose run app pip-compile requirements.in

## pip-upgrade: upgrade all requirements
pip-upgrade:
	docker compose run app pip-compile -U requirements.in

## pip-sync: sync requirements in local environment
pip-sync:
	pip-sync requirements.txt