from typing import List, Annotated
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr

from ..custom_types import Gender
from .account import AccountBaseResponse


class User(BaseModel):
    name: str
    surname: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User, LoginUser):
    pass


class UpdateUser(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    gender: str | None = None
    birthdate: datetime | None = None
    profession: str | None = None
    country: str | None
    city: str | None = None

    @classmethod
    def as_form(
        cls,
        name: Annotated[str | None, Form()] = None,
        surname: Annotated[str | None, Form()] = None,
        email: Annotated[EmailStr | None, Form()] = None,
        gender: Annotated[Gender | None, Form()] = None,
        birthdate: Annotated[datetime | None, Form()] = None,
        profession: Annotated[str | None, Form()] = None,
        country: Annotated[str | None, Form()] = None,
        city: Annotated[str | None, Form()] = None,
    ) -> "UpdateUser":
        return cls(
            name=name,
            surname=surname,
            email=email,
            gender=gender,
            birthdate=birthdate,
            profession=profession,
            country=country,
            city=city,
        )


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


class VerifyUser(BaseModel):
    email: EmailStr