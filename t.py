import pika

# Подключение к RabbitMQ серверу
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

if connection.is_open:
    print("Successfully connected to RabbitMQ", connection.is_open)

    # Создание канала
    channel = connection.channel()

    # Определение обменника fanout
    channel.exchange_declare(exchange='fanout', exchange_type='fanout')

    # Проверка наличия обменника
    exchange = channel.exchange_declare(exchange='fanout', passive=True)
    if exchange:
        print("Exchange 'fanout' is defined")

    # Отправка сообщения в обменник
    message = "Test message to RabbitMQ"
    channel.basic_publish(exchange='fanout', routing_key='', body=message)
    print(f"Message '{message}' sent to 'fanout' exchange")

    # Закрытие соединения с RabbitMQ сервером
    connection.close()
else:
    print("Failed to connect to RabbitMQ")
