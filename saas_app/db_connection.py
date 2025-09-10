from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./saas_app/saas_app.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

sessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()