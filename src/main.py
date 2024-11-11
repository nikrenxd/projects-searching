from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api.projects import project_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # start
    yield
    # end


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.include_router(project_router)
    _app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    return _app


app = create_app()
