# ====================================================================================
# Запуск FastApi локально:
# uvicorn main:app --reload
# ====================================================================================

# Подключение библиотек
from fastapi import FastAPI
from pydantic import BaseModel
from redis_manager import RedisManager

# Создание образа fastapi
app = FastAPI()

# Создание образа Redis
redis_manager = RedisManager()

# ====================================================================================

@app.on_event("startup")
async def startup_event():
    await redis_manager.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await redis_manager.close()

# ====================================================================================

class Message(BaseModel):
    message: str

@app.post("/messages/")
async def receive_message(message: Message):
    await redis_manager.save_message(message.message)
    return {"message": "Message received successfully"}

@app.get("/messages/")
async def get_messages():
    return await redis_manager.get_messages()

# ====================================================================================