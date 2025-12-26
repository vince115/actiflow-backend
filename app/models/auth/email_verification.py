# app/models/auth/email_verification.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EmailVerification(BaseModel, Base):
    """
    Email 驗證紀錄（系統級）

    用途：
    - Submission Email Verify
    - User Register Verify
    - Password Reset
    - 未來流程（invite / approve / share）
    """

    __tablename__ = "email_verifications"

    # ---------------------------------------------------------
    # Reference（通用指向）
    # ---------------------------------------------------------
    ref_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        comment="驗證對象類型：submission / user / password_reset",
    )

    ref_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="對應資料 UUID",
    )

    # ---------------------------------------------------------
    # Email & Token
    # ---------------------------------------------------------
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
