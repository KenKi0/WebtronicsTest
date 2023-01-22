# This file presents CLI shortcuts.
# Go there to find more details: https://makefiletutorial.com/#variables

migrate:
	docker-compose -f ./deployment/docker-compose.yml exec webtronics alembic upgrade head

app:
	docker-compose -f ./deployment/docker-compose.yml up -d --build
	make migrate