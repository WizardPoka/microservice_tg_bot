# ====================================================================================
# Запуск бота 
# python telegram_bot.py
# ====================================================================================


import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN

import logging
# ====================================================================================
# API_URL = "http://microservice_tg_bot-fastapi:8000/messages/"
# API_URL = "http://localhost:8000/messages/"

# API_URL = "http://127.0.0.1:8000/messages/"
API_URL = "http://fastapi:8000/messages/"
# response = requests.get(API_URL)


bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s ')

# ====================================================================================

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

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Получить список")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы получить список сообщений из FastAPI", reply_markup=keyboard)

# ====================================================================================

@bot.message_handler(func=lambda message: message.text == '/get_messages')
def get_messages(message):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            messages = response.json()
            if messages:
                bot.send_message(message.chat.id, "Сообщения из FastAPI:\n" + "\n".join(messages))
            else:
                bot.send_message(message.chat.id, "Нет сообщений из FastAPI")
        else:
            bot.send_message(message.chat.id, "Не удалось получить сообщения из FastAPI")
    except Exception as e:
        logging.exception("An error occurred while getting messages: %s", str(e))
        bot.send_message(message.chat.id, "Произошла ошибка при получении сообщений из FastAPI")

# ====================================================================================

if __name__ == "__main__":
    bot.polling()

# ====================================================================================