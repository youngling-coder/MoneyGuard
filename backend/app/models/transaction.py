from sqlalchemy import BigInteger, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as builtinEnum
from .base import Base
from .mixins import AccountRelationMixin


class TransactionType(builtinEnum):
    INCOME = "income"
    EXPENSE = "expense"


class Trasaction(AccountRelationMixin, Base):

    _account_back_populates = "transactions"

    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    description: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(Enum(TransactionType), nullable=False)
    recipient: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'