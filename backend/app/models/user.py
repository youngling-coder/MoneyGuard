from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy import Date, String, Boolean, text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..custom_types import Gender

if TYPE_CHECKING:
    from .account import Account
    from .security_code_session import Security_Code_Session


class User(Base):

    # NOTE: total balance won't be stored here as there could be a problem
    # with a transactions synchronization, in order to get total balance
    # of all the accounts it will be calculated and returned to the client

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email_confirmed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false"), default=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    profession: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(Enum(Gender), nullable=True)
    birthdate: Mapped[Date | None] = mapped_column(Date, nullable=True)
    profile_picture: Mapped[str | None] = mapped_column(String, nullable=True)
    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="owner")
    security_code_sessions: Mapped["Security_Code_Session"] = relationship(
        "Security_Code_Session", back_populates="owner"
    )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, name="{self.name}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, name="{self.name}")'
