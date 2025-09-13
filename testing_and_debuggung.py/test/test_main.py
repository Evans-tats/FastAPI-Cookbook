import pytest
from httpx import ASGITransport,AsyncClient
from Main import app

@pytest.mark.asyncio
async def test_read_root():
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response = await client.get("/home")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Mum!"}

def test_read_main_client(test_client):
    response = test_client.get("/home")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Mum!"}