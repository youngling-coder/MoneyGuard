from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
    name: str
    surname: str
    profession: Optional[str]
    country: Optional[str]
    city: Optional[str]
    birthdate: Optional[datetime]


class CreateUser(User):
    email: EmailStr
    password: str


class UserResponse(User):
    id: int
    email: str
    profile_picture: Optional[str]
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(User):
    email: EmailStr


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
