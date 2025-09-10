from pydantic import BaseModel,ConfigDict

class UserSchema(BaseModel):
    username: str
    email: str
    password: str

class showUserSchema(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)