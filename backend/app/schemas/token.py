from pydantic import BaseModel
from .user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    id: int | None
