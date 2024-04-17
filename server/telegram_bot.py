# ====================================================================================
# Запуск бота локально: 
# python telegram_bot.py
# ====================================================================================

import asyncio
import telebot
import requests
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from redis_manager import RedisManager

# ====================================================================================

# URL FastAPI
# API_URL = "http://localhost:8000/messages/"
# API_URL = "http://127.0.0.1:8000/messages/"
API_URL = "http://fastapi:8000/messages/"

# Создаем экземпляр RedisManager
redis_manager = RedisManager()

bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s ')

# ====================================================================================

# Обрабатываем все остальные сообщения от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if message.text == "Получить список":
            get_messages(message)

        elif message.text == "/get_messages":
            get_messages(message)

        elif message.text == "/start":
            handle_start(message)

        else:
            response = requests.post(API_URL, json={"message": message.text})
            if response.status_code == 200:
                bot.reply_to(message, "Ваше сообщение отправлено в FastAPI")
            else:
                bot.reply_to(message, "Не удалось отправить сообщение в FastAPI")
    except Exception as e:
        logging.exception("An error occurred while handling the message: %s", str(e))
        bot.reply_to(message, "Произошла ошибка при обработке вашего сообщения")

# ====================================================================================

# Выполняем подключение к Redis при запуске бота
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Получить список")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы получить список сообщений из Redis", reply_markup=keyboard)

# ====================================================================================

# Создаем глобальный цикл событий
global_loop = asyncio.get_event_loop()

# Обрабатываем команду /get_messages для получения сообщений из Redis
@bot.message_handler(func=lambda message: message.text == '/get_messages')
def get_messages(message):
    try:
        # Вызываем метод get_messages синхронно, используя глобальный цикл событий
        messages = global_loop.run_until_complete(redis_manager.get_messages())
        
        if messages:
            bot.send_message(message.chat.id, "Сообщения из Redis:\n" + "\n".join(messages))
        else:
            bot.send_message(message.chat.id, "Нет сообщений в Redis")
    except Exception as e:
        logging.exception("An error occurred while getting messages from Redis: %s", str(e))
        bot.send_message(message.chat.id, "Произошла ошибка при получении сообщений из Redis")

# ====================================================================================

if __name__ == "__main__":
    # Подключаемся к Redis при запуске бота
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(redis_manager.connect())
    except Exception as e:
        logging.exception("An error occurred while connecting to Redis: %s", str(e))

    # Запускаем бот
    bot.polling()

# ====================================================================================