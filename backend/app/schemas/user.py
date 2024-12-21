from pydantic import BaseModel, ConfigDict, EmailStr
from .account import AccountResponse
from datetime import datetime
from typing import List


class User(BaseModel):
    name: str
    surname: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User, LoginUser):
    pass


class UpdateUser(User):
    email: EmailStr
    profession: str | None
    country: str | None
    city: str | None
    birthdate: datetime | None


class UserBaseResponse(UpdateUser):
    id: int
    profile_picture: str | None
    timestamp: datetime


class UserAccountsResponse(UserBaseResponse):
    accounts: List[AccountResponse] | None = None
    model_config = ConfigDict(from_attributes=True)


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
