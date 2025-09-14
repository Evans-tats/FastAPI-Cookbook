import pytest
from httpx import ASGITransport,AsyncClient
from Main import app, Item
from .conftest import test_db_session

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

@pytest.mark.intergration
def test_add_item_and_read(test_client, test_db_session):
    response = test_client.get("/items/1")
    assert response.status_code == 404
    response = test_client.post("/items", json={"name": "Ball", "color": "Red"})
    assert response.status_code == 201

    item_id = response.json().get("id")
    item = (test_db_session.query(Item).filter(Item.id == item_id).first())
    assert item is not None

    response = test_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"id": item_id, "name": "Ball", "color": "Red"}


