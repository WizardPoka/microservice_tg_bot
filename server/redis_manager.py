# ====================================================================================
# Это асинхронный клиент Redis для работы с Redis в асинхронном стиле в Python
import aioredis

# Это оператор импортирует класс List из модуля typing, который мы будем использовать для указания типа возвращаемого значения метода get_messages.
from typing import List

# ====================================================================================

# Управляет подключением к Redis и выполнением операций с данными
class RedisManager:
    def __init__(self, host="redis", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis = None

# ====================================================================================

    async def connect(self):
        self.redis = aioredis.Redis.from_url(f'redis://{self.host}:{self.port}/{self.db}', decode_responses=True)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def save_message(self, message: str):
        await self.redis.lpush('messages', message)

    async def get_messages(self) -> List[str]:
        messages = await self.redis.lrange('messages', 0, -1)
        return messages

    async def clear_messages(self):
        await self.redis.delete('messages')

# ====================================================================================