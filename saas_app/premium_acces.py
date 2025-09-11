from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .operations import add_user
from .db_connection import get_db
from. db_model import Role
from . Schema import showUserSchema, UserSchema, registerResponseSchema
router = APIRouter()

@router.post("/register/premium-user/", status_code=status.HTTP_201_CREATED, response_model=registerResponseSchema)
def register_premiuim_user( user : UserSchema, session : Session = Depends(get_db)) -> registerResponseSchema:
    user.role=Role.premium.value
    user = add_user(session, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or Email already registered"
        )
    # return showUserSchema.model_validate(user)
    return {
        "message": "Premium user registered successfully",
        "user": showUserSchema.model_validate(user)
    }

