from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    message: str

messages = []

@app.post("/messages/")
async def receive_message(message: Message):
    messages.append(message.message)
    return {"message": "Message received successfully"}

@app.get("/messages/")
async def get_messages():
    return messages
