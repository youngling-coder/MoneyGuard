from typing import Annotated
from io import BytesIO
import os

from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from ..database import get_db
from .. import models, schemas, utils, smtp, verification
from ..oauth2 import oauth2


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/verify/{token}", status_code=status.HTTP_204_NO_CONTENT)
async def verify_email(token: Annotated[str, Path()], db: AsyncSession = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not authenticated to confirm an email"
    )
    email_to_verify = verification.verify_confirmation_token(token=token, credentials_exception=credentials_exception)

    if email_to_verify != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current user email and confirmation email don't match!"
        )
    
    stmt = update(models.User).where(models.User.id == current_user.id).values(email_confirmed=True)
    
    await db.execute(stmt)
    await db.commit()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: schemas.CreateUser, db: AsyncSession = Depends(get_db)):

    stmt = select(models.User).filter(models.User.email == user.email)
    result = await db.execute(stmt)
    user_exists = result.scalars().first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with a given email already exists!",
        )

    hashed_password = utils.get_password_hash(password=user.password)

    new_user = models.User(**user.model_dump())
    new_user.password = hashed_password

    db.add(new_user)
    await db.commit()

    verification_token = verification.generate_confirmation_token(email=new_user.email)
    email_confirmation_url = f"{router.prefix}/verify/{verification_token}"
    email_template = smtp.EmailTemplates.EMAIL_VERIFICATION_TEMPLATE

    email_template = email_template.replace("email_confirmation_url", email_confirmation_url)

    smtp.send_email(
        to=new_user.email,
        subject="Email Confirmation",
        content=email_template
    )


@router.put(
    "/update", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
async def update_user(
    updated_user: schemas.UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    target_user_stmt = select(models.User).filter(models.User.id == current_user.id)
    target_user_result = await db.execute(target_user_stmt)
    target_user = target_user_result.scalars().first()

    email_updated = target_user.email != updated_user.email

    stmt = (
        update(models.User)
        .where(models.User.id == target_user.id)
        .values(updated_user.model_dump())
        .execution_options(synchronize_session="fetch")
        .returning(models.User)
    )
    updated_user_stmt = await db.execute(stmt)

    if email_updated:
        verification_token = verification.generate_confirmation_token(email=updated_user.email)
        email_confirmation_url = f"{router.prefix}/verify/{verification_token}"
        email_template = smtp.EmailTemplates.EMAIL_VERIFICATION_TEMPLATE

        email_template = email_template.replace("email_confirmation_url", email_confirmation_url)

        smtp.send_email(
        to=updated_user.email,
        subject="Email Confirmation",
        content=email_template
        )

    updated_user = updated_user_stmt.scalars().first()

    await db.commit()

    return updated_user


@router.get("/get", response_model=schemas.UserResponse)
async def get_user(
    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)
):

    stmt = select(models.User).filter(models.User.id == current_user.id)
    result = await db.execute(stmt)
    requested_user = result.scalars().first()

    return requested_user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)
):

    stmt = delete(models.User).where(models.User.id == current_user.id).returning(models.User)
    
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user.profile_picture:
        os.remove(user.profile_picture)
    
    await db.commit()


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_passowrd(
    password_form: schemas.UpdatePassword,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    stmt_user = select(models.User).filter(models.User.id == current_user.id)
    result_user = await db.execute(stmt_user)
    user = result_user.scalars().first()

    if not utils.verify_password(password_form.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is wrong!"
        )

    new_password = utils.get_password_hash(password_form.new_password)

    stmt = (
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(password=new_password)
    )

    await db.execute(stmt)
    await db.commit()


@router.patch("/profile_picture")
async def update_profile_picture(
    profile_picture: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    SUPPORTED_FILE_TYPES = ("image/png", "image/jpeg")

    if profile_picture.content_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file type. Allowed types: image/jpeg, image/png",
        )

    image_bytes = await profile_picture.read()

    if len(image_bytes) > 2 ** 20:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Image is too large! Maximal file size is {((2 ** 20) / (10 ** 6)):.2f}MB "
        )
    
    image = Image.open(BytesIO(image_bytes))
    save_path = utils.get_profile_picture_url(current_user.id)

    stmt = select(models.User).filter(models.User.id == current_user.id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    try:
        image.save(save_path)

        user.profile_picture = save_path
        await db.commit()
        await db.refresh(user)

    except Exception as ex:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while image processing",
        )


@router.delete("/profile_picture")
async def delete_profile_picture(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    save_path = utils.get_profile_picture_url(current_user.id)

    try:
        os.remove(save_path)

    finally:
        stmt = select(models.User).filter(models.User.id == current_user.id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        user.profile_picture = None

        await db.commit()
        await db.refresh(user)
