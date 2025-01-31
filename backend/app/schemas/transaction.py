from pydantic import BaseModel
from datetime import datetime
from ..custom_types import TransactionType, TransactionCategory


class Transaction(BaseModel):
    amount: float
    category: TransactionCategory
    sender_recipient: str


class CreateTransaction(Transaction):
    type: TransactionType
    primary_account_number: str


class TransactionResponse(Transaction):
    id: int
    timestamp: datetime


class UpdateTransaction(CreateTransaction):
    pass
