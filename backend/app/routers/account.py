from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, schemas
from ..database import get_db
from ..oauth2 import oauth2

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_account(account: schemas.CreateAccount, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    stmt = select(models.Account).filter(models.Account.primary_account_number == account.primary_account_number)
    result = await db.execute(stmt)
    account_exists = result.scalars().first()

    if account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This ccount already exists!"
        )
    
    new_account = models.Account(**account.model_dump())
    new_account.owner_id = current_user.id

    db.add(new_account)
    await db.commit()