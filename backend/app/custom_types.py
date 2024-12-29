from enum import Enum


class TransactionType(Enum):
    income = "income"
    expense = "expense"


class Gender(Enum):
    male = "male"
    female = "female"
