from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..custom_types import TransactionType


class Transaction(BaseModel):
    amount: float
    description: str | None
    sender_recipient: str | None


class CreateTransaction(Transaction):
    type: TransactionType


class TransactionResponse(CreateTransaction):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateTransaction(CreateTransaction):
    pass
