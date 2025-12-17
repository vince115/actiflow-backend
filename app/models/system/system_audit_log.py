# app/models/system/system_audit_log.py

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


class SystemAuditLog(BaseModel, Base):
    """
    系統層級操作日誌
    - 記錄 super_admin / system_admin / support 等對平台資源的操作
    - 不綁定 Event / Submission（那是 domain audit）
    """

    __tablename__ = "system_audit_logs"

    # ---------------------------------------------------------
    # External audit code（企業級追蹤用）
    # ---------------------------------------------------------
    audit_code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Operator
    # ---------------------------------------------------------
    user_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user: Mapped[Optional["User"]] = relationship(
        lazy="selectin",
    )

    user_email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    user_role: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    # ex: super_admin / system_admin / support / auditor

    # ---------------------------------------------------------
    # Action
    # ---------------------------------------------------------
    action: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    # ex: update_system_settings / create_platform / modify_membership

    # ---------------------------------------------------------
    # Target
    # ---------------------------------------------------------
    target_type: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    # ex: Platform / SystemSettings / SystemMembership

    target_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        nullable=True,
    )

    # ---------------------------------------------------------
    # Snapshot
    # ---------------------------------------------------------
    before_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    after_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Security info
    # ---------------------------------------------------------
    ip_address: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Extra
    # ---------------------------------------------------------
    extra: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
