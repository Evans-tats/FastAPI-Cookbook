import pytest
from fastapi.testclient import TestClient
from Main import app

@pytest.fixture(scope="function")
def test_client():
    client = TestClient(app)
    yield client
    # Teardown can be done here if necessary

