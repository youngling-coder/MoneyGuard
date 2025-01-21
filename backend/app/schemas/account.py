from typing import List

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .transaction import TransactionResponse


class Account(BaseModel):
    title: str
    card_verification_value: str
    expiration_date: datetime


class CreateAccount(Account):
    primary_account_number: str
    balance: float


class AccountBaseResponse(Account):
    id: int
    balance: float
    primary_account_number: str
    timestamp: datetime


class AccountTransactionsResponse(AccountBaseResponse):
    transactions: List[TransactionResponse]
    model_config = ConfigDict(from_attributes=True)


class UpdateAccount(Account):
    pass
