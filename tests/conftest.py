import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

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


@pytest.fixture(scope="session")
async def client(app, base_url, **kwargs):
    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url=base_url, **kwargs) as c:
            yield c
