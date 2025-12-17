# app/models/system/system_config_version.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
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


class SystemConfigVersion(BaseModel, Base):
    """
    系統設定版本（versioning for SystemSettings / Platform settings）
    - 和 Event 無關
    - 不需要子表
    """

    __tablename__ = "system_config_versions"

    # ---------------------------------------------------------
    # Version identity
    # ---------------------------------------------------------
    version_code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Target reference
    # ---------------------------------------------------------
    target_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    # ex: "SystemSettings", "Platform"

    target_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        nullable=True,
    )

    # ---------------------------------------------------------
    # Operator info
    # ---------------------------------------------------------
    user_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        nullable=True,
    )

    user_email: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Snapshot
    # ---------------------------------------------------------
    config_snapshot: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Security / Audit
    # ---------------------------------------------------------
    ip_address: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
