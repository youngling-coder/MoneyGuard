from datetime import datetime
from typing import Annotated
from io import BytesIO
import os
from PIL import Image

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Form,
    HTTPException,
    status,
    File,
    UploadFile,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete

from ..database import get_db
from .. import models, schemas, utils, smtp, verification
from ..oauth2 import oauth2


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/verify/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def verify_email(
    token: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not authenticated to confirm an email",
    )
    email_to_verify = verification.verify_confirmation_token(
        token=token, credentials_exception=credentials_exception
    )

    if email_to_verify != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current user email and confirmation email don't match!",
        )

    stmt = (
        update(models.User)
        .where(models.User.id == current_user.id)
        .execution_options(synchronize_session="fetch")
        .values(email_confirmed=True)
    )

    await db.execute(stmt)
    await db.commit()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: Annotated[schemas.CreateUser, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    stmt = select(models.User).filter(models.User.email == user.email)
    result = await db.execute(stmt)
    user_exists = result.scalars().first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with a given email already exists!",
        )

    hashed_password = utils.get_hash(plain=user.password)

    new_user = models.User(**user.model_dump())
    new_user.password = hashed_password

    db.add(new_user)
    await db.commit()

    verification_token = verification.generate_confirmation_token(email=new_user.email)
    email_confirmation_url = f"{router.prefix}/verify/{verification_token}"
    email_template = smtp.EmailTemplates.SIGNUP_EMAIL_VERIFICATION_TEMPLATE

    email_template = email_template.replace(
        "email_confirmation_url", email_confirmation_url
    )

    await smtp.send_email(
        to=new_user.email, subject="Email Confirmation", content=email_template
    )


@router.put(
    "/update", status_code=status.HTTP_200_OK, response_model=schemas.UserBaseResponse
)
async def update_user(
    name: Annotated[str, Form(...)],
    surname: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    birthdate: Annotated[datetime, Form(...)],
    profession: Annotated[str, Form(...)],
    country: Annotated[str, Form(...)],
    city: Annotated[str, Form(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
    profile_picture: Annotated[UploadFile, File(...)],
):

    SUPPORTED_FILE_TYPES = ("image/png", "image/jpeg")
    if profile_picture:
        if profile_picture.content_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unsupported file type. Allowed types: {SUPPORTED_FILE_TYPES}",
            )

        image_bytes = await profile_picture.read()

        if len(image_bytes) > 2**20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Image is too large! Maximal file size is {((2 ** 20) / (10 ** 6)):.2f}MB ",
            )

        image = Image.open(BytesIO(image_bytes))
        save_path = utils.get_profile_picture_path(current_user.id)

        try:
            image.save(save_path)

        except Exception as ex:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong while image processing",
            )

    profile_picture = utils.get_profile_picture_url(current_user.id)
    updated_user_schema = schemas.UpdateUser(
        name=name,
        surname=surname,
        email=email,
        birthdate=birthdate,
        profession=profession,
        country=country,
        city=city,
        profile_picture=profile_picture,
    )
    updated_user_stmt = (
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(updated_user_schema.model_dump())
        .execution_options(synchronize_session="fetch")
        .returning(models.User)
    )

    email_updated = current_user.email != email

    updated_user_result = await db.execute(updated_user_stmt)
    await db.commit()

    updated_user = updated_user_result.scalars().first()

    if email_updated:
        verification_token = verification.generate_confirmation_token(
            email=updated_user.email
        )
        email_confirmation_url = f"{router.prefix}/verify/{verification_token}"
        email_template = smtp.EmailTemplates.EMAIL_VERIFICATION_TEMPLATE

        email_template = email_template.replace(
            "email_confirmation_url", email_confirmation_url
        )

        await smtp.send_email(
            to=updated_user.email, subject="Email Confirmation", content=email_template
        )

    return updated_user


@router.get("/get", response_model=schemas.UserBaseResponse)
async def get_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = (
        select(models.User)
        .filter(models.User.id == current_user.id)
        .options(selectinload(models.User.accounts))
    )
    result = await db.execute(stmt)
    requested_user = result.scalars().first()

    return requested_user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = (
        delete(models.User)
        .where(models.User.id == current_user.id)
        .returning(models.User)
    )

    result = await db.execute(stmt)
    user = result.scalars().first()

    if user.profile_picture:
        os.remove(user.profile_picture)

    await db.commit()


@router.patch("/reset_password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    reset_password_data: Annotated[schemas.ResetPassword, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!"
    )
    token_data = oauth2.verify_access_token(
        reset_password_data.security_code_session_token,
        credentials_exception=credentials_exception,
    )
    stmt = select(models.User).filter(models.User.id == token_data.id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    security_code_session_stmt = select(models.Security_Code_Session).filter(
        models.Security_Code_Session.security_code_session_token
        == reset_password_data.security_code_session_token
    )
    security_code_session_result = await db.execute(security_code_session_stmt)
    security_code_session = security_code_session_result.scalars().first()

    if not security_code_session:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security code session not found!",
        )

    if not security_code_session.is_verified:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Security code is invalid!"
        )

    new_password = utils.get_hash(reset_password_data.new_password)

    user.password = new_password

    security_code_session_delete_stmt = delete(models.Security_Code_Session).where(
        models.Security_Code_Session.id == security_code_session.id
    )
    await db.execute(security_code_session_delete_stmt)
    await db.commit()
    await db.refresh(user)


@router.delete("/profile_picture")
async def delete_profile_picture(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    save_path = utils.get_profile_picture_path(current_user.id)

    try:
        os.remove(save_path)

    finally:
        stmt = select(models.User).filter(models.User.id == current_user.id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        user.profile_picture = None

        await db.commit()
        await db.refresh(user)
