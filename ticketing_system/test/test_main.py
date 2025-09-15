import pytest
import asyncio

def test_sanity():
    assert 2 + 2 == 4

@pytest.mark.asyncio
async def test_read_ticket(test_client):
    response = await test_client.get("/ticket/1")
    assert response.status_code == 404 

@pytest.mark.asyncio
async def test_add_ticket(test_client):
    payload = {"price": 50.0, "user": "Alice", "show": "Concert"}
    response = await test_client.post("/ticket", json=payload)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_delete_task(test_client):
    response = await test_client.delete("ticket/1")
    assert response.status_code == 200