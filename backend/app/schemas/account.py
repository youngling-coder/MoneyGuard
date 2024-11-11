from pydantic import BaseModel, ConfigDict
from datetime import datetime
from custom_types import AccountType


class Account(BaseModel):
    title: str


class CreateAccount(Account):
    primary_card_number: str
    account_type: AccountType


class AccountResponse(Account):
    balance: int
    primary_account_number: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UpdateAccount(CreateAccount):
    balance: int