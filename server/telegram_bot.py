
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import telebot
import requests

TOKEN = "7118436747:AAEQvWAAw3UtnU_JjzYN7if-dP52vjGE_JY"
API_URL = "http://127.0.0.1:8000/messages/"

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Получить список":
        get_messages(message)
    elif message.text == "/get_messages":
        get_messages(message)
    elif message.text == "/start":
        handle_start(message)
    else:
        response = requests.post(API_URL, json={"message": message.text})
        if response.status_code == 200:
            bot.reply_to(message, "Your message has been sent to FastAPI")
        else:
            bot.reply_to(message, "Failed to send message to FastAPI")

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Получить список")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы получить список сообщений из FastAPI", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == '/get_messages')
def get_messages(message):
    response = requests.get(API_URL)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            bot.send_message(message.chat.id, "Messages from FastAPI:\n" + "\n".join(messages))
        else:
            bot.send_message(message.chat.id, "No messages from FastAPI")
    else:
        bot.send_message(message.chat.id, "Failed to fetch messages from FastAPI")


if __name__ == "__main__":
    bot.polling()
