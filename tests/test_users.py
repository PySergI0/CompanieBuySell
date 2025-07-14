import pytest
from httpx import AsyncClient, ASGITransport

from main import app

def func(d: int):
    return 1 / d

@pytest.mark.asyncio
async def test_func():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api",
    ) as ac:
        response = await ac.get("/users")
        assert response.status_code == 200
        # print(response)
