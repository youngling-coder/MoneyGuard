from typing import Optional
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


def create_access_token(data: dict):
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
) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token,
            application_settings.jwt_secret_key,
            algorithms=[application_settings.jwt_algo],
        )
        id: str = payload.get("id")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except JWTError as jwt_err:
        raise credentials_exception

    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token: Optional[TokenData] = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )

    stmt = select(models.User).filter(models.User.id == token.id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    return user
