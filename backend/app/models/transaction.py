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
    sender_recipient: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=False)
