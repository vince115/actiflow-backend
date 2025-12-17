# app/models/auth/auth_log.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.user.user import User
# ---------------------------------------------------------

class AuthLog(BaseModel, Base):
    """
    登入 / 登出 / refresh token / 驗證相關行為紀錄
    """

    __tablename__ = "auth_logs"

    # ---------------------------------------------------------
    # Foreign Key
    # ---------------------------------------------------------
    user_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Event type
    # ---------------------------------------------------------
    event: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    """
    login_success
    login_failed
    logout
    refresh
    password_reset_request
    password_reset_success
    email_verified
    """

    # ---------------------------------------------------------
    # Request info
    # ---------------------------------------------------------
    ip: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    detail: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="auth_logs",
        lazy="selectin",
    )
