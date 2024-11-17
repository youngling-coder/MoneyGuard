from datetime import timezone
from datetime import datetime, timedelta

from jose import jwt
from pydantic import EmailStr
from fastapi import HTTPException

from ..settings import application_settings


def generate_confirmation_token(email: EmailStr):
    to_encode = {"email": email}

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=application_settings.email_confirmation_url_expiration_time
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        application_settings.jwt_secret_key,
        algorithm=application_settings.jwt_algo,
    )


def verify_confirmation_token(
    token: str, credentials_exception: HTTPException
) -> EmailStr:
    try:
        payload = jwt.decode(
            token,
            application_settings.jwt_secret_key,
            algorithms=[application_settings.jwt_algo],
        )

        email: EmailStr = payload.get("email")

    except:
        raise credentials_exception

    return email
