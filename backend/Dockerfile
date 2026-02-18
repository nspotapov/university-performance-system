# Базовый образ для сборки
FROM python:3.12.3-slim-bookworm AS builder

# Установка системных зависимостей для сборки
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.12.3-slim-bookworm

# Установка только необходимых системных пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование виртуального окружения из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создание пользователя для безопасности
RUN groupadd -r fastapi \
    && useradd -r -g fastapi fastapi

# Создание рабочей директории
WORKDIR /app

# Копирование приложения
COPY --chown=fastapi:fastapi . .

RUN chmod +x entrypoint.sh

# Переключение на непривилегированного пользователя
USER fastapi

ENTRYPOINT ["/app/entrypoint.sh"]

# Экспорт порта
EXPOSE 8000

# Переменные окружения
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
