from datetime import datetime
from typing import Annotated
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path

from .. import models, schemas
from ..utils import get_balance_change_ratio
from ..database import get_db
from ..oauth2 import oauth2
from ..custom_types import TransactionCategory

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_account(
    account: Annotated[schemas.CreateAccount, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = select(models.Account).filter(
        models.Account.primary_account_number == account.primary_account_number,
        models.Account.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    account_exists = result.scalars().first()

    if account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account already exists!",
        )

    new_account = models.Account(**account.model_dump())
    new_account.owner_id = current_user.id

    try:
        db.add(new_account)
        await db.commit()
        await db.refresh(new_account)

        if new_account.balance:
            first_transaction = models.Transaction(
                amount=new_account.balance,
                sender_recipient=f"{current_user.name} {current_user.surname}",
                owner_id=new_account.id,
                category=TransactionCategory.income.value,
                user_id=current_user.id,
            )
            db.add(first_transaction)

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )


@router.get("/get_all", response_model=list[schemas.AccountBaseResponse])
async def get_accounts(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
    limit: Annotated[int, Query()] = 10,
    offset: Annotated[int, Query()] = 0,
):

    stmt = (
        select(models.Account)
        .where(models.Account.owner_id == current_user.id)
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    accounts = result.scalars().all()

    return accounts


@router.get("/total_balance")
async def get_total_balance(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
    month: Annotated[int, Query()] = None,
):

    change_ratio = Decimal("100.0")

    stmt = (
        select(models.Account)
        .filter(models.Account.owner_id == current_user.id)
        .options(selectinload(models.Account.transactions))
    )

    result = await db.execute(stmt)
    accounts = result.scalars().all()

    total_balance = Decimal("0.0")

    for account in accounts:
        total_balance += account.balance

    if month:
        transactions: list[models.Transaction] = []

        for account in accounts:
            transactions.extend(account.transactions)

        total_balance, change_ratio = get_balance_change_ratio(
            total_balance=total_balance, month=month, transactions=transactions
        )

    return {"amount": total_balance, "change_ratio": change_ratio}


@router.get("/{primary_account_number}/", response_model=schemas.AccountBaseResponse)
async def get_account(
    primary_account_number: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = select(models.Account).where(
        models.Account.primary_account_number == primary_account_number,
        models.Account.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    account = result.scalars().first()

    if not account:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found!"
        )

    if account.owner_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to get access to this account!",
        )

    return account


@router.delete(
    "/delete/{primary_account_number}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(
    primary_account_number: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = select(models.Account).filter(
        models.Account.primary_account_number == primary_account_number,
        models.Account.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    account_exists = result.scalars().first()

    if not account_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found!"
        )

    stmt = delete(models.Account).where(
        models.Account.primary_account_number == primary_account_number
    )
    await db.execute(stmt)
    await db.commit()


@router.put(
    "/update/{primary_account_number}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccountBaseResponse,
)
async def update_account(
    primary_account_number: Annotated[str, Path()],
    account: Annotated[schemas.UpdateAccount, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[models.User, Depends(oauth2.get_current_user)],
):

    stmt = select(models.Account).filter(
        models.Account.primary_account_number == primary_account_number,
        models.Account.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    account_exists = result.scalars().first()

    if not account_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found!"
        )

    stmt = (
        update(models.Account)
        .where(models.Account.primary_account_number == primary_account_number)
        .values(account.model_dump())
        .execution_options(synchronize_session="fetch")
        .returning(models.Account)
    )
    result = await db.execute(stmt)
    await db.commit()

    account = result.scalars().first()

    return account
