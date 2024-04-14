


import telebot
import requests

TOKEN = "7118436747:AAEQvWAAw3UtnU_JjzYN7if-dP52vjGE_JY"
API_URL = "http://127.0.0.1:8000/messages/"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    data = {"message": message.text}
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        bot.reply_to(message, "Your message has been sent to FastAPI")
    else:
        bot.reply_to(message, "Failed to send message to FastAPI")

if __name__ == "__main__":
    bot.polling()
