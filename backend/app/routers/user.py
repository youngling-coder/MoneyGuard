from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from ..database import get_db
from .. import models, schemas, utils
from ..oauth2 import oauth2


router = APIRouter(prefix="/users", tags=["Users"])


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
    print(new_user.timestamp)

    db.add(new_user)
    await db.commit()


@router.put(
    "/update", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
async def update_user(
    updated_user: schemas.UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    target_user_stmt = select(models.User).filter(models.User.id == current_user.id)
    target_user_result = await db.execute(target_user_stmt)
    target_user = target_user_result.scalars().first()

    stmt = (
        update(models.User)
        .where(models.User.id == target_user.id)
        .values(updated_user.model_dump())
        .execution_options(synchronize_session="fetch")
        .returning(models.User)
    )

    updated_user_stmt = await db.execute(stmt)
    updated_user = updated_user_stmt.scalars().first()

    await db.commit()

    return updated_user


@router.get("/get", response_model=schemas.UserResponse)
async def get_user(
    db: AsyncSession = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):

    stmt = select(models.User).filter(models.User.id == current_user.id)
    result = await db.execute(stmt)
    requested_user = result.scalars().first()

    return requested_user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):

    stmt = delete(models.User).where(models.User.id == current_user.id)
    await db.execute(stmt)
    await db.commit()


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_passowrd(
    password_form: schemas.UpdatePassword,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
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
