from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    full_name: str


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