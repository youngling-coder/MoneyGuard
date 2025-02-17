from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class ExpiredToken(Base):

    token: Mapped[str] = mapped_column(String, unique=True)
