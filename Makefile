postgres:
	docker run --name pdb -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_USER=${DB_USER} -e POSTGRES_DB=${DB_NAME} -d --rm -p5432:5432 postgres

test:
	poetry run pytest tests/test.py -v

app:
	docker compose up --build

include .env
local_up:
	poetry run python src/wsgi.py

include .env
postgres:
	docker run --name pdb -e POSTGRES_PASSWORD=${DB_PASSWORD} -e POSTGRES_USER=${DB_USER} -e POSTGRES_DB=${DB_NAME} -d --rm -p${DB_PORT}:5432 postgres
