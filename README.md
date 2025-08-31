# ResumeApp

ResumeApp is a FastAPI-based application for managing resumes. It includes user authentication, resume CRUD operations, and PostgreSQL as the database. The project is fully containerized with Docker, making it easy to run and test on any machine.

---

## Features

* User registration and authentication (JWT)
* CRUD operations for resumes
* Role-based access (admin/user)
* Fully containerized with Docker
* Alembic migrations for database schema
* Automated tests with pytest

---

## Prerequisites

* [Docker](https://www.docker.com/get-started) installed
* [Docker Compose](https://docs.docker.com/compose/install/)
* Optional: Python 3.11+ for local development

---

## Setup & Run with Docker

1. Clone the repository:

```bash
git clone <your-repo-url>
cd ResumeApp
```

2. Build and start the containers:

```bash
docker compose build
docker compose up -d
```

3. Apply database migrations:

```bash
docker compose run --rm web bash -c "cd backend && alembic upgrade head"
```

4. Run automated tests (optional but recommended):

```bash
docker compose run --rm web bash -c "cd /app && pytest -v"
```

---

## Accessing the Application

* FastAPI runs on port 8000. Open in your browser or API client:

```
http://localhost:8000
```

* Swagger UI docs:

```
http://localhost:8000/docs
```

* Redoc API docs:

```
http://localhost:8000/redoc
```

---

## Alembic Migrations

* Migration scripts are located in `backend/alembic/versions`.
* To create a new migration:

```bash
docker compose run --rm web bash -c "cd backend && alembic revision -m 'your_message_here'"
docker compose run --rm web bash -c "cd backend && alembic upgrade head"
```

* The `role` column in `users` is handled safely by the migration system.

---

## Database Notes

* Each developer gets an **isolated Postgres database** via Docker.
* The database is automatically created when the container starts.
* Alembic migrations create all tables and columns, including `role`.
* Initial data can be added using the admin user or seed scripts.

---

## Running Locally (Without Docker)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn backend.app.main:app --reload
```

3. Apply migrations:

```bash
alembic upgrade head
```

4. Run tests:

```bash
pytest -v
```

---

## Tests

* Tests are located in `backend/tests/`.
* They cover authentication, CRUD operations, and role-based access.
* Run tests with:

```bash
cd backend
pytest -v
```

---

## Additional Notes

* Ensure Postgres is running before applying migrations.
* The database password is set in `docker-compose.yml` and can be safely changed.
* For fresh setups, Alembic will create all tables and columns, so the app is ready to run.



# ResumeApp

ResumeApp — это приложение на FastAPI для управления резюме. Оно включает аутентификацию пользователей, операции CRUD для резюме и базу данных PostgreSQL. Проект полностью контейнеризован с помощью Docker, что позволяет легко запускать и тестировать его на любой машине.

---

## Функции

* Регистрация и аутентификация пользователей (JWT)
* Операции CRUD для резюме
* Доступ на основе ролей (админ/пользователь)
* Полная контейнеризация с Docker
* Миграции базы данных с Alembic
* Автоматические тесты с pytest

---

## Требования

* [Docker](https://www.docker.com/get-started) установлен
* [Docker Compose](https://docs.docker.com/compose/install/)
* Необязательно: Python 3.11+ для локальной разработки

---

## Установка и запуск через Docker

1. Клонируйте репозиторий:

```bash
git clone <your-repo-url>
cd ResumeApp
```

2. Постройте и запустите контейнеры:

```bash
docker compose build
docker compose up -d
```

3. Примените миграции базы данных:

```bash
docker compose run --rm web bash -c "cd backend && alembic upgrade head"
```

4. Запустите автоматические тесты (по желанию):

```bash
docker compose run --rm web bash -c "cd /app && pytest -v"
```

---

## Доступ к приложению

* FastAPI работает на порту 8000. Откройте в браузере или API-клиенте:

```
http://localhost:8000
```

* Swagger UI документация:

```
http://localhost:8000/docs
```

* Redoc API документация:

```
http://localhost:8000/redoc
```

---

## Миграции Alembic

* Скрипты миграций находятся в `backend/alembic/versions`.
* Чтобы создать новую миграцию:

```bash
docker compose run --rm web bash -c "cd backend && alembic revision -m 'ваше_сообщение'"
docker compose run --rm web bash -c "cd backend && alembic upgrade head"
```

* Колонка `role` в таблице пользователей обрабатывается безопасно через миграции.

---

## Замечания о базе данных

* Каждый разработчик получает **отдельную базу Postgres** через Docker.
* База создается автоматически при старте контейнера.
* Миграции Alembic создают все таблицы и колонки, включая `role`.
* Начальные данные можно добавить через админ-пользователя или seed-скрипты.

---

## Запуск локально (без Docker)


1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Запустите приложение:

```bash
uvicorn backend.app.main:app --reload
```

3. Примените миграции:

```bash
alembic upgrade head
```

4. Запустите тесты:

```bash
pytest -v
```

---

## Тесты

* Тесты находятся в `backend/tests/`.
* Они покрывают аутентификацию, операции CRUD и доступ на основе ролей.
* Запуск тестов:

```bash
cd backend
pytest -v
```

---

## Дополнительно

* Убедитесь, что Postgres запущен перед применением миграций.
* Пароль базы данных указан в `docker-compose.yml` и может быть безопасно изменен.
* Для новой установки Alembic создаст все таблицы и колонки, приложение будет готово к запуску.
