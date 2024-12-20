# Запуск всего приложения
run:
	docker-compose up --build -d

# Остановка всех контейнеров
stop:
	docker-compose down

# Запуск тестов
test:
	docker-compose -f docker-compose.test.yml up --build --exit-code-from web_test

# Просмотр логов
logs:
	docker-compose logs -f

# Очистка Docker (удаление неиспользуемых контейнеров, сетей и образов)
clean:
	docker system prune -f

# Создание миграций базы данных
db-migrate:
	docker-compose exec web flask db migrate -m "Migration"

# Применение миграций
db-upgrade:
	docker-compose exec web flask db upgrade

# Откат миграций
db-downgrade:
	docker-compose exec web flask db downgrade

# Просмотр статуса базы данных
db-status:
	docker-compose exec web flask db current

# Запуск интерактивной оболочки в контейнере web
shell:
	docker-compose exec web /bin/bash

.PHONY: run stop test logs clean db-migrate db-upgrade db-downgrade db-status shell