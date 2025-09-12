from fastapi import (APIRouter, Depends, HTTPException, status)
from sqlalchemy.orm import Session
from typing import Annotated

from .db_connection import get_db
from .security import (decode_acces_token, oauth2_scheme)
from . Schema import showUserSchema, MessageResponseSchema
from .db_model import Role

def get_current_user(token:str =  Depends(oauth2_scheme), session : Session = Depends(get_db)):
    user = decode_acces_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details ="user not authorized"
        )
    return showUserSchema.model_validate(user)

def get_premium_user(user : Annotated[get_current_user, Depends()]):
    if user.role != Role.premium.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to premium features"
        )
    return {
        "message" : f"you're logged in as {user.username}, welcome to premium features",
        "user" : showUserSchema.model_validate(user)
    }

router = APIRouter()
@router.get("/welcome/all-users", response_model=MessageResponseSchema)
def all_users_can_access(user: Annotated[get_current_user, Depends()]):
    return {
        "message" : f"you're logged in as {user.username}",
        "user" : showUserSchema.model_validate(user)
    }

@router.get("/welcome/premium-users", response_model=MessageResponseSchema)
def premium_users_can_access(user: Annotated[get_premium_user, Depends()]):
    return user