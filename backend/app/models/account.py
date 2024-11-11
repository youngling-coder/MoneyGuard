from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
from .mixins import UserRelationMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class Account(UserRelationMixin, Base):

    _user_back_populates = "accounts"

    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=0)
    primary_card_number: Mapped[str] = mapped_column(String, nullable=False)

    transactions: Mapped[list["Transaction"]] = mapped_column(
        "Transaction", back_populates="owner"
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'
