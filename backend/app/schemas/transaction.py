from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..custom_types import TransactionType, TransactionCategory


class Transaction(BaseModel):
    amount: float
    category: TransactionCategory
    sender_recipient: str


class CreateTransaction(Transaction):
    type: TransactionType


class TransactionResponse(CreateTransaction):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateTransaction(CreateTransaction):
    pass
