from contextlib import asynccontextmanager
from fastapi import FastAPI,status, Depends, HTTPException
# from db_connection import get_db, engine
# import db_model
from . import db_connection, db_model, operations, Schema
from sqlalchemy.orm import Session

# from .operations import add_user
# from Schema import showUserSchema, UserSchema 


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_model.Base.metadata.create_all(db_connection.engine)
    yield 

app = FastAPI(title="SaaS Application", version="1.0.0", lifespan=lifespan)

@app.post("/register/users/", status_code=status.HTTP_201_CREATED, response_model=Schema.showUserSchema)
def register_user(User : Schema.UserSchema, session : Session = Depends(db_connection.get_db)):
    user = operations.add_user(session, User)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Username or Email already registered"
        )
    return Schema.showUserSchema.model_validate(user)