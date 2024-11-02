from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.projects import project_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # start
    yield
    # end


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.include_router(project_router)

    return _app


app = create_app()
