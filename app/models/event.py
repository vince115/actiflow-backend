# app/models/event.py （活動主表）

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base_model import BaseModel

class Event(BaseModel, Base):
    """
    活動主表（企業級）
    - id / uuid：由 BaseModel 提供（PK）
    - event_code：業務代號（例如 EVT-2025-001）
    - organizer_uuid：主辦單位
    - activity_template_uuid：所套用的活動模板
    """
    __tablename__ = "events"

    # ---------------------------------------------------------
    # 業務用活動代號（外部顯示、不變）
    # ---------------------------------------------------------
    event_code = Column(String, unique=True, nullable=False, index=True)

    # 活動狀態：draft / published / closed
    status = Column(String, nullable=False, default="draft")

    # ---------------------------------------------------------
    # 外鍵：主辦單位
    # ---------------------------------------------------------
    organizer_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    organizer = relationship("Organizer", back_populates="events", lazy="selectin")

    # ---------------------------------------------------------
    # 外鍵：所套用的活動模板
    # ---------------------------------------------------------
    activity_template_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_templates.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    activity_template = relationship("ActivityTemplate", back_populates="events", lazy="selectin")

    # ---------------------------------------------------------
    # 活動基本資訊
    # ---------------------------------------------------------
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    # 報名截止日
    registration_deadline = Column(DateTime, nullable=True)

    # 活動其他設定
    config = Column(JSONB, nullable=True)

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    fields = relationship(
        "EventField",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    submissions = relationship(
        "Submission",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete"
    )