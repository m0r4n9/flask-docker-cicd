# Flask Application with CI/CD

## Локальная разработка

```bash
# Запуск приложения
make dev

# Запуск тестов
make test

# Сборка и публикация образа
make build
make push
```

## Деплой

1. Настройте секреты в GitHub:
   - DOCKER_USERNAME
   - DOCKER_PASSWORD
   - SERVER_HOST
   - SERVER_USER
   - SSH_PRIVATE_KEY

2. Push в main ветку автоматически запустит процесс CI/CD:
   - Запуск тестов
   - Сборка Docker образа
   - Публикация в Docker Hub
   - Деплой на сервер

## Мониторинг

- Логи: `docker-compose logs -f`
- Статус: `docker-compose ps`
- Метрики: http://your-domain/metrics
- Grafana: http://your-domain:3000

## Обновление

Ручной деплой:
```bash
make deploy
```

## Откат

```bash
# Откат к предыдущей версии
docker-compose down
docker-compose pull
docker-compose up -d --force-recreate
```