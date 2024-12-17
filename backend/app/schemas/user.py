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


class UserResponse(UpdateUser):
    id: int
    profile_picture: str | None
    timestamp: datetime
    accounts: List[AccountResponse]

    model_config = ConfigDict(from_attributes=True)


class VerifySecurityCode(BaseModel):
    email: EmailStr
    security_code: str

    
class ResetPassword(BaseModel):
    email: str
    new_password: str
