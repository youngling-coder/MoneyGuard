from jose import JWTError, jwt
from datetime import timezone
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..schemas.token import TokenData
from ..database import get_db
from .. import models
from ..settings import application_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=application_settings.jwt_expiration_time)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, application_settings.jwt_secret_key, algorithm=application_settings.jwt_algo)


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData | None:
    try:
        payload = jwt.decode(token, application_settings.jwt_secret_key, algorithms=[application_settings.jwt_algo])
        id: str = payload.get("id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)

    except JWTError as jwt_err:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
