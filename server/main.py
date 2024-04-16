# ====================================================================================
# Запуск FastApi локально:
# uvicorn main:app --reload
# ====================================================================================

# Подключение библиотек
from fastapi import FastAPI
from pydantic import BaseModel

# Создание образа fastapi
app = FastAPI()

# ====================================================================================

class Message(BaseModel):
    message: str

messages = []

# Метод приема сообщений
@app.post("/messages/")
async def receive_message(message: Message):
    messages.append(message.message)
    return {"message": "Message received successfully"}

# Метод вывода всех сообщений
@app.get("/messages/")
async def get_messages():
    return messages

# ====================================================================================