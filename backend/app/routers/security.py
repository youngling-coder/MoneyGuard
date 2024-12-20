from typing import Annotated

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path

from .. import models, schemas, smtp, utils
from ..database import get_db
from ..oauth2 import oauth2


router = APIRouter(prefix="/security", tags=["Security"])


@router.post("/send_security_code", status_code=status.HTTP_200_OK)
async def send_security_code(
    security_code_data: Annotated[schemas.SendSecurityCode, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    stmt = select(models.User).filter(models.User.email == security_code_data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    security_code = utils.generate_security_code(length=6)

    content = smtp.EmailTemplates.RESET_PASSWORD_SECURITY_CODE_TEMPLATE
    content = content.replace("security_code", security_code)

    user.security_code = utils.get_hash(security_code)
    user.security_code_verified = False

    await db.commit()
    await db.refresh(user)

    await smtp.send_email(
        to=security_code_data.email,
        subject="Your security code for password reset",
        content=content,
    )


@router.post("/verify_security_code", status_code=status.HTTP_200_OK)
async def verify_security_code(
    security_code_data: Annotated[schemas.user.VerifySecurityCode, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    stmt = select(models.User).filter(models.User.email == security_code_data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    if not utils.verify_hash(security_code_data.security_code, user.security_code):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Security code is invalid!"
        )

    user.security_code_verified = True
    user.security_code = None

    await db.commit()
    await db.refresh(user)


@router.patch("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    reset_password_data: Annotated[schemas.ResetPassword, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    stmt = select(models.User).filter(models.User.email == reset_password_data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    if not user.security_code_verified:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Security code is invalid!"
        )

    new_password = utils.get_hash(reset_password_data.new_password)

    user.password = new_password
    user.security_code_verified = False

    await db.commit()
    await db.refresh(user)
