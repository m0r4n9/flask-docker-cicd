#!/bin/bash

# Остановка и удаление старых контейнеров
docker-compose down

# Удаление старых образов
docker system prune -f

# Получение последних образов
docker-compose pull

# Запуск новых контейнеров
docker-compose up -d

# Проверка статуса
docker-compose ps