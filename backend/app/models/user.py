from typing import TYPE_CHECKING, Optional

from .base import Base
from sqlalchemy import Date, String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .account import Account


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
    profession: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    birthdate: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="owner")

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, full_name="{self.full_name}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, full_name="{self.full_name}")'
