from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport
import pytest_asyncio  
import pytest

from app.Main import app
from app.database import Base
from app.db_connection import get_db_session

test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass = StaticPool,
    connect_args = {"check_same_thread": False}
)
testLocalSession = async_sessionmaker(autoflush=False, 
                                          autocommit=False, 
                                          bind=test_engine, 
                                          class_= AsyncSession)

@pytest_asyncio.fixture
async def test_db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with testLocalSession() as session:
        yield session 
    

@pytest.fixture
def test_client(test_db_session):
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    app.dependency_overrides[get_db_session] = lambda: test_db_session
    yield client