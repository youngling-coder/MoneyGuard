from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    name: str
    surname: str


class CreateUser(User):
    email: str
    password: str


class UserResponse(User):
    id: int
    email: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(CreateUser):
    pass
