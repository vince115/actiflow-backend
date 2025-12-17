# app/models/event/event_staff.py

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
    from app.models.event.event import Event
    from app.models.user.user import User
# ---------------------------------------------------------



class EventStaff(BaseModel, Base):
    """
    活動工作人員 / 講師 / 領隊 / 志工
    """

    __tablename__ = "event_staffs"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 可選：關聯到 User
    # ---------------------------------------------------------
    user_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ---------------------------------------------------------
    # 工作人員基本資料
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # 職務（leader / assistant / staff / speaker / medical…）
    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # 職務說明
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # 排序
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # 是否啟用
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # 可擴充欄位
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        back_populates="staffs",
        lazy="selectin",
    )

    user: Mapped[Optional["User"]] = relationship(
        back_populates="event_staffs",
        lazy="selectin",
    )