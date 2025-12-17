# app/models/auth/user_session.py

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
    from app.models.auth.refresh_token import RefreshToken
# ---------------------------------------------------------
class UserSession(BaseModel, Base):
    """
    使用者登入 Session（多裝置登入管理）
    - 每次 login 產生一筆
    - 可用於：裝置管理、強制登出、異常登入偵測
    """

    __tablename__ = "user_sessions"

    # ---------------------------------------------------------
    # Foreign Key → User
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Session 資訊
    # ---------------------------------------------------------
    user_agent: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # 對應 refresh token（不是 token 本體）
    refresh_token_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("refresh_tokens.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # 是否仍有效（登出 / 強制中斷）
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # 最近一次使用（refresh 時更新）
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Session 到期時間（選用）
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        back_populates="sessions",
        lazy="selectin",
    )

    refresh_token: Mapped[Optional["RefreshToken"]] = relationship(
        back_populates="user_sessions",
        lazy="selectin",
    )
