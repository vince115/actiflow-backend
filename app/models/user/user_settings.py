# app/models/user/user_settings.py

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


class UserSettings(BaseModel, Base):
    """
    使用者個人偏好設定（1 對 1）
    """

    __tablename__ = "user_settings"

    # ---------------------------------------------------------
    # Foreign Key（1:1 User）
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Basic preferences
    # ---------------------------------------------------------
    dark_mode: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    locale: Mapped[str] = mapped_column(
        String,
        default="zh-Hant",
    )

    # ---------------------------------------------------------
    # Notification preferences
    # ---------------------------------------------------------
    notify_email: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    notify_sms: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    notify_marketing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ---------------------------------------------------------
    # UI / extra config
    # ---------------------------------------------------------
    ui_preferences: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        back_populates="settings",
        lazy="selectin",
    )
