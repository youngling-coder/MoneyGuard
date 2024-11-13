from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class User(BaseModel):
    name: str
    surname: str


class CreateUser(User):
    email: EmailStr
    password: str


class UserResponse(User):
    id: int
    email: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(User):
    email: EmailStr

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str