# app/models/event/event_schedule.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventSchedule(BaseModel, Base):
    """
    活動場次 / 行程 / Session
    - 可用於多場活動、多天活動、分場活動
    """

    __tablename__ = "event_schedules"

    # ---------------------------------------------------------
    # 外鍵：Event
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 場次名稱（上午場 / Day 1 / 台北場）
    title = Column(String(255), nullable=False)

    # 內容描述（行程說明、注意事項…）
    description = Column(String, nullable=True)

    # 開始 / 結束時間
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)

    # 場地資訊
    location = Column(String(255), nullable=True)

    # 可擴充欄位（地圖、講師資訊、配速分組、補給站資訊等）
    config = Column(JSONB, default=lambda: {})

    # 排序
    sort_order = Column(Integer, default=0)

    # 是否啟用顯示
    is_enabled = Column(Boolean, default=True)

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="schedules",
        lazy="selectin"
    )
