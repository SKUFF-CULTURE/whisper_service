.PHONY: build run stop logs shell kafka-logs

# Имя контейнера и образа
CONTAINER_NAME=svo
IMAGE_NAME=svo-container

# Сборка Docker-образов через docker-compose
build:
	docker build -t whisperer .

run:
	docker run --gpus all whisperer