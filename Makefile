# This file presents CLI shortcuts.
# Go there to find more details: https://makefiletutorial.com/#variables

migrate:
	docker-compose exec worker alembic upgrade head

app:
	docker-compose build
	docker-compose up -d
	make migrate