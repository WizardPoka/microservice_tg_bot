FROM rabbitmq:management

# Установка плагина отправки сообщений на почту
RUN rabbitmq-plugins enable rabbitmq_email

# Копируем файл конфигурации rabbitmq.conf в контейнер
COPY rabbitmq.conf /etc/rabbitmq/

# Открываем порт для веб-интерфейса управления
EXPOSE 15672
