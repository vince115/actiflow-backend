# app/models/event/event_report.py

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

class EventReportCache(BaseModel, Base):
    """
    活動報表快取（非正式資料，會定期重算）
    - 前台 / 後台的活動統計數據會寫在這裡
    - 不影響 Submission / Price / Field 的正式資料
    """

    __tablename__ = "event_report_cache"

    # ---------------------------------------------------------
    # 外鍵：活動（一對一）
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,   # ⭐ 一對一關係的關鍵
    )

    # ---------------------------------------------------------
    # 報名統計資料（JSON）
    # ---------------------------------------------------------
    report_data: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="report_cache",
        lazy="selectin",
    )
