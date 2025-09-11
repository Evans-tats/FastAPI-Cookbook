from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
# from Schema import showUserSchema,UserSchema
from .Schema import showUserSchema,UserSchema
from saas_app.db_model import User

def add_user(session: Session,user : UserSchema) -> showUserSchema | None:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password, role=user.role)
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)

    except IntegrityError:
        session.rollback()
        return None
    
    return showUserSchema.model_validate(db_user)

def get_user(session : Session, username: str) -> showUserSchema | None:
    user = session.query(User).filter(User.username == username).first()
    if user:
        return showUserSchema.model_validate(user)
    return None