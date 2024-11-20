from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .transaction import Transaction


class Account(UserRelationMixin, Base):

    _user_back_populates = "accounts"

    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("0")
    )
    primary_account_number: Mapped[str] = mapped_column(String, nullable=False)
    card_verification_value: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="owner"
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'
