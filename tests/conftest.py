import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

from src.core.db import engine, Base, Session
from src.core.config import settings
from src.main import create_app


@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def session():
    async with Session() as session:
        yield session


@pytest.fixture(scope="session")
async def client(app, base_url, **kwargs):
    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url=base_url, **kwargs) as c:
            yield c
