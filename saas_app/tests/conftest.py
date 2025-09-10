import pytest
from sqlalchemy import create_engine,QueuePool
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from .. import db_model, Schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def session():
    engine = create_engine("sqlite:///./test.db", 
                           connect_args={"check_same_thread": False},
                           echo=True,
                           poolclass=QueuePool)
    sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db_session = sessionLocal()
    db_model.Base.metadata.create_all(engine)
    yield db_session
    db_model.Base.metadata.drop_all(engine)
    db_session.close()

@pytest.fixture(scope="function")
def fill_database_session(session):
    (session.add(
        Schema.UserSchema(
            username="chrissophia",
            email="chrissophia@email.com",
            hashed_password=pwd_context.hash(
                "hellomum"
            )
        )
    ))
    (session.add(
        Schema.UserSchema(
            username="johnwick",
            email="johnwick007@gmail.com",
            hashed_password=pwd_context.hash("helloimunderthewater")
        )
    ))
    
    (session.add(
        Schema.UserSchema(
            username="manucourtney",
            email="mcourtney@email.com",
            hashed_password=pwd_context.hash("harderpass")
        )
    ))
    session.commit()
    yield session