from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
