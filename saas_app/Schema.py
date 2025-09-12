from pydantic import BaseModel,ConfigDict

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    role: str | None = "basic"

class showUserSchema(BaseModel):
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class MessageResponseSchema(BaseModel):
    message: str
    user: showUserSchema