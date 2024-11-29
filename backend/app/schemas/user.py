from pydantic import BaseModel, ConfigDict, EmailStr
from .account import AccountResponse
from datetime import datetime
from typing import List


class User(BaseModel):
    name: str
    surname: str


class CreateUser(User):
    email: EmailStr
    password: str


class UpdateUser(User):
    email: EmailStr
    profession: str | None
    country: str | None
    city: str | None
    birthdate: datetime | None


class UserResponse(UpdateUser):
    id: int
    profile_picture: str | None
    timestamp: datetime
    accounts: List[AccountResponse]

    model_config = ConfigDict(from_attributes=True)


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
