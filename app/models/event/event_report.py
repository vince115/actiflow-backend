# app/models/event/event_report.py

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventReportCache(BaseModel, Base):
    """
    活動報表快取（非正式資料，會定期重算）
    - 前台 / 後台的活動統計數據會寫在這裡
    - 不影響 Submission / Price / Field 的正式資料
    """

    __tablename__ = "event_report_cache"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 報名統計資料（JSON 格式）
    # ---------------------------------------------------------
    # 例如：
    # {
    #   "total": 120,
    #   "by_price": {"early_bird": 45, "normal": 60, "vip": 15},
    #   "by_schedule": {"day1": 70, "day2": 50},
    #   "gender": {"male": 70, "female": 50},
    #   "age": {"20-29": 30, "30-39": 50, "40+": 40}
    # }
    report_data = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="report_cache",
        lazy="selectin"
    )
