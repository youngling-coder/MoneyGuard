from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Account(BaseModel):
    title: str
    primary_account_number: str
    card_verification_value: str
    expiration_date: datetime


class CreateAccount(Account):
    pass


class AccountResponse(Account):
    balance: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateAccount(Account):
    balance: int
