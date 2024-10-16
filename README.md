# Документация по проекту Balance Manager

## Описание

Данный проект представляет собой веб-приложение, написанное на Django, с использованием PostgreSQL в качестве базы данных. Он включает API для работы с балансом пользователей и их перемещением.

## Стек технологий

- Django
- PostgreSQL
- Poetry
- Docker
- Django REST Framework

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone git@github.com:poligrafo/balance_manager.git
   ```
2. **Скопируйте файл примера переменных окружения:**

   ```bash
   cp .env_example .env
   ```
3. **Настройте файл .env:**

Отредактируйте файл .env, чтобы установить необходимые переменные окружения. По умолчанию он должен выглядеть так:

   ```makefile
DEBUG=1
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
   ```
## Запуск проекта
После выполнения всех вышеуказанных шагов, запустите проект с помощью Docker:

   ```bash
docker-compose up --build
   ```
## Использование API
Документация по API доступна через Swagger. Вы можете получить доступ к ней по следующему URL:

   ```bash
http://localhost:8000/swagger/
   ```