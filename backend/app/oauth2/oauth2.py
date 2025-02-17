from typing import Annotated
from datetime import timezone
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.token import TokenData
from ..database import get_db
from .. import models
from ..settings import application_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=application_settings.jwt_expiration_time
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        application_settings.jwt_secret_key,
        algorithm=application_settings.jwt_algo,
    )


def verify_access_token(
    token: str, credentials_exception: HTTPException
) -> TokenData | None:
    try:
        payload = jwt.decode(
            token,
            application_settings.jwt_secret_key,
            algorithms=[application_settings.jwt_algo],
        )
        id: int = payload.get("id")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)], token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data: TokenData | None = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )

    stmt = select(models.ExpiredToken).filter(models.ExpiredToken.token == token)
    result = await db.execute(stmt)
    token = result.scalars().first()

    if token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token provided!"
        )

    stmt = select(models.User).filter(models.User.id == token_data.id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    return user
