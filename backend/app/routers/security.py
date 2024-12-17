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
    to: Annotated[EmailStr, Query()], db: Annotated[AsyncSession, Depends(get_db)]
):

    stmt = select(models.User).filter(models.User.email == to)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    security_code = utils.generate_security_code(length=6)

    content = smtp.EmailTemplates.RESET_PASSWORD_VERIFICATION_CODE_TEMPLATE
    content = content.replace("verification_code", security_code)

    user.security_code = utils.get_hash(security_code)
    await db.commit()
    await db.refresh(user)

    await smtp.send_email(
        to=to, subject="Your security code for password reset", content=content
    )
