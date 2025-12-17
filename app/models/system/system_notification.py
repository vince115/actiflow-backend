# app/models/system/system_notification.py

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

class SystemNotification(BaseModel, Base):
    """
    全平台公告（維護、更新、重要訊息）
    """

    __tablename__ = "system_notifications"

    # ---------------------------------------------------------
    # External identity
    # ---------------------------------------------------------
    notification_code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Content
    # ---------------------------------------------------------
    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Notification level
    # ---------------------------------------------------------
    level: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="info",  # info / warning / critical / success
    )

    # ---------------------------------------------------------
    # Visibility
    # ---------------------------------------------------------
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Config
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
