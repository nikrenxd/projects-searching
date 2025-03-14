from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.projects import project_router
from src.core.redis import RedisClient
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    RedisClient.redis_init()
    yield
    # end
    await RedisClient.redis_close()


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.add_middleware(CORSMiddleware, allow_origins=[settings.FE_TRUSTED_URL])

    _app.include_router(project_router)

    return _app


app = create_app()
