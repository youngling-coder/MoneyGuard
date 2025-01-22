from sqlalchemy import Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from decimal import Decimal
from .mixins import AccountRelationMixin


class Transaction(AccountRelationMixin, Base):

    _account_back_populates = "transactions"

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2), nullable=False, server_default=text("0.00")
    )
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    sender_recipient: Mapped[str | None] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'
