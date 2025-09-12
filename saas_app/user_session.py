from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . db_connection import get_db
from.operations import get_user
from rbac import get_current_user
from . Schema import showUserSchema, MessageResponseSchema

router = APIRouter()
@router.post("/login")
async def login(user : showUserSchema = Depends(get_current_user), session :Session = Depends(get_db)):
    db_user = get_user(session, user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        "message" : f"Welcome back {user.username}",
        "user" : showUserSchema.model_validate(db_user)
    }