# ====================================================================================

# Базовый образ Python для телеграм-бота
FROM python:3.9-slim as bot

# Установка зависимостей для телеграм-бота
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копирование исходного кода телеграм-бота в контейнер
COPY server /app

# Запуск телеграм-бота
CMD ["python", "telegram_bot.py"]

# ====================================================================================

# Перенести потом в докер файл для RabbitMQ

# # Базовый образ RabbitMQ
# FROM rabbitmq:management as rabbitmq

# # Установка плагина отправки сообщений на почту
# RUN rabbitmq-plugins enable rabbitmq_email

# # Копирование файла конфигурации rabbitmq.conf в контейнер
# COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# # Открытие порта для веб-интерфейса управления
# EXPOSE 15672

