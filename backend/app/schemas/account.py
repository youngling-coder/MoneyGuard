from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Account(BaseModel):
    title: str


class CreateAccount(Account):
    primary_card_number: str


class AccountResponse(Account):
    balance: int
    primary_account_number: str
    card_verification_number: str
    expiration_date: datetime
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateAccount(CreateAccount):
    balance: int
