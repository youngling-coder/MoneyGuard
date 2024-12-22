from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Query,
    status,
    Path,
    Response,
    Cookie,
)
from fastapi.responses import JSONResponse

from .. import models, schemas, utils, smtp
from ..database import get_db
from ..oauth2 import oauth2


router = APIRouter(prefix="/security_code_sessions", tags=["Security Code Session"])


@router.post(
    "/create",
    status_code=status.HTTP_200_OK,
)
async def create_security_code_session(
    response: Response,
    request_security_code_session_data: Annotated[
        schemas.RequestSecurityCodeSession, Body()
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    stmt = select(models.User).filter(
        models.User.email == request_security_code_session_data.email
    )
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    security_code_session_stmt = select(models.Security_Code_Session).filter(
        models.Security_Code_Session.owner_id == user.id
    )
    security_code_session_result = await db.execute(security_code_session_stmt)
    security_code_session = security_code_session_result.scalars().first()

    security_code = utils.generate_security_code(length=6)
    security_code_session_token = oauth2.create_token({"id": user.id})

    content = smtp.EmailTemplates.SECURITY_CODE_SESSION_REQUEST_TEMPLATE
    content = content.replace("security_code", security_code)

    security_code = utils.get_hash(security_code)

    if security_code_session:
        security_code_session.security_code = security_code
        security_code_session.security_code_session_token = security_code_session_token
        security_code_session.is_verified = False

        await db.commit()
        await db.refresh(security_code_session)

    else:
        security_code_session = schemas.CreateSecurityCodeSession(
            email=request_security_code_session_data.email,
            security_code=security_code,
            security_code_session_token=security_code_session_token,
        )

        new_session = models.Security_Code_Session(**security_code_session.model_dump())
        new_session.owner_id = user.id

        db.add(new_session)
        await db.commit()

    await smtp.send_email(
        to=request_security_code_session_data.email,
        subject="Your security code for password reset",
        content=content,
    )

    response.set_cookie(
        key="security_code_session_token",
        value=security_code_session_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_security_code_session(
    security_code_data: Annotated[schemas.VerifySecurityCodeSession, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
    security_code_session_token: Annotated[str, Cookie()] = None,
):

    stmt = select(models.Security_Code_Session).filter(
        models.Security_Code_Session.security_code_session_token
        == security_code_session_token
    )
    result = await db.execute(stmt)
    security_code_session = result.scalars().first()

    if not security_code_session:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    if not utils.verify_hash(
        security_code_data.security_code, security_code_session.security_code
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Security code is invalid!"
        )

    security_code_session.is_verified = True

    await db.commit()
    await db.refresh(security_code_session)
