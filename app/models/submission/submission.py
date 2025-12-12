# app/models/submission.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class Submission(BaseModel, Base):
    """
    報名紀錄模型
    """
    __tablename__ = "submissions"

    # 業務代碼（顯示用，不是 PK）
    submission_code = Column(String, unique=True, nullable=False, index=True)

    # 所屬 Event
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    event = relationship("Event", back_populates="submissions", lazy="selectin")

    # 報名者資訊
    user_email = Column(String, nullable=False, index=True)

    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    user = relationship("User", back_populates="submissions", lazy="selectin")

    # 狀態
    status = Column(
        Enum(
            "pending", 
            "paid",
            "canceled",
            "completed",
            "waitlist",
            name="submission_status"
        ),
        default="pending",
        nullable=False
    )
    status_reason = Column(Text, nullable=True)

    # 後台備註
    notes = Column(Text, nullable=True)

    # 安全紀錄
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)

    submitted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # 自訂額外資料
    extra_data = Column(JSONB, default=lambda: {})

    # Relationship
    values = relationship(
        "SubmissionValue",
        back_populates="submission",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    tickets = relationship(
        "EventTicket",
        back_populates="submission",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    files = relationship(
    "SubmissionFile",
    back_populates="submission",
    lazy="selectin",
    cascade="all, delete-orphan"
)
