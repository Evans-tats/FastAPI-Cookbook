from fastapi import FastAPI
from fastapi import Depends, HTTPException, status, Request
from schema import itemschema, responseitemschema
from sqlalchemy.orm import Session
from app_logging import client_logger

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String, index=True)

DATABASE_URL = "sqlite:///./Mydatabase.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/home")
async def read_root():
    return {"Hello": "Mum!"}

@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=responseitemschema)
def add_item(item: itemschema, session: Session = Depends(get_db)):
    db_item = Item(name=item.name, color=item.color)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return responseitemschema.model_validate(db_item)

@app.get("/items/{item_id}", response_model=responseitemschema ,status_code=status.HTTP_200_OK)
def get_item(item_id: int, session: Session = Depends(get_db)):
    item_db = (session.query(Item).filter(Item.id == item_id).first())
    if not item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return responseitemschema.model_validate(item_db)

@app.middleware("http")
async def log_requests(request : Request, call_next):
    client_logger.info(
        f"method : {request.method}, "
        f"call : {request.url.path}, "
        f"ip : {request.client.host}"
    )
    response = await call_next(request)
    return response