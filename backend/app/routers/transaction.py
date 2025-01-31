from datetime import datetime
from typing import Annotated
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy import delete, update
from sqlalchemy.future import select
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path

from .. import models, schemas
from ..database import get_db
from ..oauth2 import oauth2
from ..custom_types import TransactionCategory, TransactionType


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/categories")
async def get_categories():

    return [category.value for category in TransactionCategory]


@router.post("/create")
async def create_transaction(transaction: Annotated[schemas.CreateTransaction, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)]
):
    stmt = select(models.Account).filter(models.Account.primary_account_number == transaction.primary_account_number)
    result = await db.execute(stmt)
    account = result.scalars().first()

    if not account:
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found!"
        )
    
    if transaction.type.value == TransactionType.expense.value:
        transaction.amount = -transaction.amount

    account.balance += Decimal(str(transaction.amount))
    
    transaction_dict = transaction.model_dump()
    transaction_dict.pop("type")
    transaction_dict.pop("primary_account_number")
    
    new_transaction = models.Transaction(**transaction_dict)
    new_transaction.category = transaction.category.value
    new_transaction.owner_id = account.id
    new_transaction.user_id = current_user.id

    db.add(new_transaction)
    await db.commit()


@router.get("/get_all", response_model=list[schemas.TransactionResponse])
async def get_all_transactions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
    limit: Annotated[int, Query()] = 10,
    offset: Annotated[int, Query()] = 0,
):

    stmt = (
        select(models.Transaction)
        .where(models.Transaction.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
    ).order_by(models.Transaction.timestamp.desc())

    result = await db.execute(stmt)
    transactions = result.scalars().all()

    return transactions
