from sqlalchemy import Numeric, String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from decimal import Decimal
from .mixins import AccountRelationMixin


class Transaction(AccountRelationMixin, Base):

    _account_back_populates = "transactions"

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2), nullable=False, server_default=text("0.00")
    )
    category: Mapped[str] = mapped_column(String, nullable=False)
    sender_recipient: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'
