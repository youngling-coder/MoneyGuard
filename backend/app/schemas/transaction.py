from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..custom_types import TransactionType
from typing import Optional


class Transaction(BaseModel):
    amount: int
    description: Optional[str]
    type: TransactionType
    recipient: Optional[str]


class CreateTransaction(Transaction):
    pass


class TransactionResponse(CreateTransaction):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateTransaction(CreateTransaction):
    pass
