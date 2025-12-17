# app/models/event/event_schedule.py

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
# ---------------------------------------------------------

class EventSchedule(BaseModel, Base):
    """
    活動場次 / 行程 / Session
    - 可用於多場活動、多天活動、分場活動
    """

    __tablename__ = "event_schedules"

    # ---------------------------------------------------------
    # 外鍵：Event
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 場次基本資訊
    # ---------------------------------------------------------
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # 時間資訊
    # ---------------------------------------------------------
    start_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    end_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ---------------------------------------------------------
    # 場地與設定
    # ---------------------------------------------------------
    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # 狀態 / 排序
    # ---------------------------------------------------------
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        back_populates="schedules",
        lazy="selectin",
    )
