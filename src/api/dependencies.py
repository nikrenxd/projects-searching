from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.db import Session
from src.core.redis import RedisClient


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


async def get_redis() -> Redis:
    return RedisClient.client


SessionDep = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]
