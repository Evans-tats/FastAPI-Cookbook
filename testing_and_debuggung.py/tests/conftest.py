import pytest
from fastapi.testclient import TestClient
from Main import app, get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///:memory",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool )

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db_session():
    Base.metadata.create_all(bind=engine)
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(test_db_session):
    client = TestClient(app)
    app.dependency_overrides[get_db] = lambda: test_db_session
    yield client
    # Teardown can be done here if necessary



