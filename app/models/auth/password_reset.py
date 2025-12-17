# app/models/auth/password_reset.py

# 密碼重設 Token（一次性）
# 使用後即失效
# 或超過 expires_at 自動失效 

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

class PasswordReset(BaseModel, Base):
    """
    密碼重設 Token（一次性）
    - 使用後即失效
    - 或超過 expires_at 自動失效
    """

    __tablename__ = "password_resets"

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
    # Reset info
    # ---------------------------------------------------------
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    # 寄給使用者的 reset token
    token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    # Token 有效期限
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # 是否已使用
    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        "User",
        back_populates="password_resets",
        lazy="selectin",
    )