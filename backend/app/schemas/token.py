from pydantic import BaseModel
from .user import UserBaseResponse


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBaseResponse


class TokenData(BaseModel):
    id: int | None
