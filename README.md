# Simple Django Application with User Registration and Authentication

This is a Django application that provides user registration and authentication functionality using JSON Web Tokens (JWT) and includes logging.

## Technology Stack

### Backend

- **Django**: A Python framework for web application development.
- **Django Rest Framework (DRF)**: A library for creating APIs in Django applications.
- **Django Simple JWT**: A library for handling JWT authentication tokens.
- **django-environ**: A library for managing environment settings.
- **PhoneNumberField**: A field for storing and validating phone numbers.
- **PostgreSQL**: A relational database for storing user data.

## Installation and Configuration

### 1. Clone the Repository:

```bash
git clone git@github.com:AlliKalykov/simple_django_project_with_auth.git
```

### 2. Create a .env File in the Project's Root Directory and Specify the Necessary Environment Settings:

```bash
SECRET_KEY=secret_key

DEBUG=on

POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_user_password
POSTGRES_HOST=localhost
POSTGRES_PORT=port

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

CORS_ORIGIN_WHITELIST=http://localhost:8000,http://0.0.0.0:8000,http://0.0.0.0:8000

# ACCESS_TOKEN_LIFETIME is 1 minute
ACCESS_TOKEN_LIFETIME=30
# REFRESH_TOKEN_LIFETIME is 1 month
REFRESH_TOKEN_LIFETIME=1

LOG_TO_FILE=True
LOG_TO_CONSOLE=True
LOG_DIR=logs/app.logs
LOG_LEVEL=INFO
```

### 3. Install Dependencies:

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations:

```bash
python manage.py migrate
```

## Logging
Application event logs are available in the myauthapp.log file. You can configure log levels and message formats in settings.py.

#

# Простое Django-приложение с регистрацией и авторизацией пользователей

Это Django-приложение, предоставляющее функциональность регистрации и авторизации пользователей с использованием JSON Web Tokens (JWT), а также подключено логирование. 

## Стек технологий

### Backend

- **Django**: Python-фреймворк для разработки веб-приложений.
- **Django Rest Framework (DRF)**: Библиотека для создания API в Django-приложениях.
- **Django Simple JWT**: Библиотека для обработки JWT-токенов аутентификации.
- **django-environ**: Библиотека для управления настройками окружения.
- **PhoneNumberField**: Поле для хранения и валидации номеров телефонов.
- **PostgreSQL**: Реляционная база данных для хранения данных пользователей.

## Установка и настройка

### 1. Клонируйте репозиторий:

```bash
git clone git@github.com:AlliKalykov/simple_django_project_with_auth.git
```

### 2. Создайте файл .env в корневой директории проекта и укажите необходимые настройки окружения:

```bash
SECRET_KEY=secret_key

DEBUG=on

POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_user_password
POSTGRES_HOST=localhost
POSTGRES_PORT=port

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

CORS_ORIGIN_WHITELIST=http://localhost:8000,http://0.0.0.0:8000,http://0.0.0.0:8000

# ACCESS_TOKEN_LIFETIME is 1 minute
ACCESS_TOKEN_LIFETIME=30
# REFRESH_TOKEN_LIFETIME is 1 month
REFRESH_TOKEN_LIFETIME=1

LOG_TO_FILE=True
LOG_TO_CONSOLE=True
LOG_DIR=logs/app.logs
LOG_LEVEL=INFO
```

### 3. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 4. Примените миграции:

```bash
python manage.py migrate
```

## Логирование
Логи событий приложения доступны в файле myauthapp.log. Вы можете настроить уровни логирования и формат сообщений в settings.py.
