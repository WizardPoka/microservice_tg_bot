# ====================================================================================

# Базовый образ Python для FastAPI
FROM python:3.9-slim

# Установка зависимостей для FastAPI
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование исходного кода FastAPI в контейнер
COPY server  /app

# Запуск FastAPI
# Важно указывать правильный путь 
# http://fastapi:8000
CMD ["uvicorn", "main:app", "--host", "fastapi", "--port", "8000"]

# ====================================================================================