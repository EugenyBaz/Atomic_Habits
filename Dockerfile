# Используем Python 3.12 slim-образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update \
  && apt-get install -y build-essential libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry глобально
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -
ENV PATH="/opt/poetry/bin:$PATH"

# Создаем виртуальное окружение и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
  && poetry install --no-root

# Копируем остальные файлы приложения
COPY . .

# Открываем порт для приложения
EXPOSE 8000