# app/models/submission.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base_model import BaseModel


class Submission(BaseModel, Base):
    """
    報名紀錄模型
    """
    __tablename__ = "submissions"

    # 企業級業務 primary key（非 PK）
    submission_code = Column(String, unique=True, nullable=False, index=True)

    # 所屬的 Event
    # 外鍵：報名對應的 Event（以 uuid 串）
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    event = relationship("Event", back_populates="submissions", lazy="selectin")

    # 報名者 email（必要）
    user_email = Column(String, nullable=False, index=True)
    # 若後續導入使用者系統，可使用 user_uuid（選擇性）
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    user = relationship("User", back_populates="submissions", lazy="selectin")

    # 狀態：pending / paid / canceled / completed / waitlist
    status = Column(String, default="pending", nullable=False)
    status_reason = Column(Text, nullable=True)   # << 新增（避免 CRUD crash）

    # --- 後台備註（審核/管理用） ---
    notes = Column(Text, nullable=True)

    # --- 安全紀錄 ---
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)

    # 提交時間（比 created_at 更明確）
    submitted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # metadata (统一名称)
    metadata = Column(JSONB, default=lambda: {})

    # 一筆 submission 對應多個欄位值
    values = relationship(
        "SubmissionValue", 
        back_populates="submission", 
        lazy="selectin", 
        cascade="all, delete-orphan"
    )
