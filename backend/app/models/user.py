from .base import Base
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .account import Account


class User(Base):

    # NOTE: total balance won't be stored here as there could be a problem
    # with a transactions synchronization, in order to get total balance
    # of all the accounts it will be calculated and returned to the client

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    logo_path: Mapped[str] = mapped_column(String, nullable=False, server_default="/logos/default.png")
    accounts: Mapped[list["Account"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, full_name="{self.full_name}")'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} (id={self.id}, full_name="{self.full_name}")'
