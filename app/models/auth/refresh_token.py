# app/models/auth/refresh_token.py

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
    from app.models.auth.user_session import UserSession
# ---------------------------------------------------------

class RefreshToken(BaseModel, Base):
    """
    Refresh Token（長期登入憑證）
    - HttpOnly Cookie 使用
    - 可撤銷（revoked）
    - 可綁定 UserSession
    """

    __tablename__ = "refresh_tokens"

    # ---------------------------------------------------------
    # Foreign Key → User（⚠️ 使用 uuid，不用舊的 user_id）
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Token data
    # ---------------------------------------------------------
    token: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy="selectin",
    )

    user_sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="refresh_token",
        lazy="selectin",
        # 不要 delete-orphan，避免 refresh_token 斷開後 session 被 ORM 誤刪
        cascade="save-update, merge",
    )
