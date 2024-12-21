from .base import Base
from sqlalchemy import String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from .mixins import UserRelationMixin


class Security_Code_Session(UserRelationMixin, Base):

    _user_back_populates = "security_code_sessions"

    security_code_session_token: Mapped[str] = mapped_column(String, nullable=False)
    security_code: Mapped[str] = mapped_column(String, nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false"), default=False
    )
