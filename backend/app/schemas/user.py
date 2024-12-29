from pydantic import BaseModel, ConfigDict, EmailStr
from .account import AccountBaseResponse
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
    profile_picture: str | None


class UserBaseResponse(UpdateUser):
    id: int
    profile_picture: str | None
    timestamp: datetime


class UserAccountsResponse(UserBaseResponse):
    accounts: List[AccountBaseResponse]
    model_config = ConfigDict(from_attributes=True)


class ResetPassword(BaseModel):
    security_code_session_token: str
    new_password: str
