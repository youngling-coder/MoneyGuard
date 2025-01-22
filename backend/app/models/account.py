from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import String, Numeric, text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .transaction import Transaction


class Account(UserRelationMixin, Base):

    _user_back_populates = "accounts"

    title: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2, asdecimal=True), nullable=False, server_default=text("0.00")
    )
    primary_account_number: Mapped[str] = mapped_column(
        String, nullable=False, unique=True
    )
    card_verification_value: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="owner"
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, balance="{self.balance}", title="{self.title}")'
