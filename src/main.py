from contextlib import asynccontextmanager

from fastapi import FastAPI


from src.api.projects import project_router
from src.core.redis import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    RedisClient.redis_init()
    yield
    # end
    await RedisClient.redis_close()


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.include_router(project_router)

    return _app


app = create_app()
