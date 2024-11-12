from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: schemas.CreateUser, db: AsyncSession = Depends(get_db)):

    stmt = select(models.User).filter(models.User.email == user.email)
    result = await db.execute(stmt)
    user_exists = result.scalars().first()

    print(user)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with a given email already exists!"
        )
    
    hashed_password = utils.get_password_hash(password=user.password)

    new_user = models.User(**user.model_dump())
    new_user.password = hashed_password
    print(new_user.timestamp)
    
    db.add(new_user)
    await db.commit()