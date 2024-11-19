from redis import asyncio as redis
from redis import exceptions

from src.core.config import settings
from src.core.logger import logger


class RedisClient:
    client: redis.Redis = None

    @classmethod
    def redis_init(cls):
        pool = redis.ConnectionPool().from_url(settings.REDIS_URL)

        try:
            cls.client = redis.Redis().from_pool(pool)
        except exceptions.ConnectionError:
            logger.error("Connection to Redis was failed")

    @classmethod
    async def redis_close(cls):
        if redis is not None:
            await cls.client.aclose()
