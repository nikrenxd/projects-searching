import pytest


pytestmark = pytest.mark.anyio


async def test_api(client):
    params = {"project_name": "Django"}
    res = await client.get("/search/", params=params)

    assert res.status_code == 200
