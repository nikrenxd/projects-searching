from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    # start
    yield
    # end


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)
    return _app


app = create_app()
