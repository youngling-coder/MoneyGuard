from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..custom_types import TransactionType


class Transaction(BaseModel):
    amount: int
    description: str | None
    type: TransactionType
    recipient: str | None


class CreateTransaction(Transaction):
    pass


class TransactionResponse(CreateTransaction):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateTransaction(CreateTransaction):
    pass
