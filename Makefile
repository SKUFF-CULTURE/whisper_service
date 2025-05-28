.PHONY: build run stop logs shell kafka-logs

# Имя контейнера и образа
CONTAINER_NAME=svo2
IMAGE_NAME=svo-container2

# Сборка Docker-образов через docker-compose
build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

flush:
	docker compose down -v

# Вывести логи всех контейнеров
logs:
	docker compose logs -f

mistral:
	docker compose exec service_ollama ollama pull mistral