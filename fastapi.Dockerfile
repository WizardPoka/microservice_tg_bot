# Базовый образ Python для FastAPI
FROM python:3.9-slim

# Установка зависимостей для FastAPI
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование исходного кода FastAPI в контейнер
COPY server /app

# Запуск FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
