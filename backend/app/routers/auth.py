from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..oauth2.login_form import OAuth2EmailRequestForm
from ..oauth2 import oauth2
from ..database import get_db
from .. import models, utils


router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_credentials: OAuth2EmailRequestForm = Depends(),
):

    stmt = select(models.User).filter(models.User.email == user_credentials.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Seems there's no user with a given email! Double check spelling!",
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password for an account with a given email!",
        )

    access_token = oauth2.create_token(data={"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
