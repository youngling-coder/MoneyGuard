from sqlalchemy import BigInteger, String, Enum, text
from sqlalchemy.orm import Mapped, mapped_column
from ..custom_types import TransactionType
from .base import Base
from .mixins import AccountRelationMixin


class Transaction(AccountRelationMixin, Base):

    _account_back_populates = "transactions"

    amount: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("0")
    )
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(Enum(TransactionType), nullable=False)
    recipient: Mapped[str | None] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, type="{self.type}", amount="{self.amount}", recipient="{self.recipient}")'
