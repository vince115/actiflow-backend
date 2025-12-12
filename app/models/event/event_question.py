# app/models/event/event_question.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventQuestion(BaseModel, Base):
    """
    活動常見問題（FAQ）、注意事項、說明區塊
    (不屬於表單欄位，純展示用)
    """

    __tablename__ = "event_questions"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 題目 / 問題
    question = Column(String(500), nullable=False)

    # 答案（可長文字）
    answer = Column(String, nullable=True)

    # 類型（可選）：faq / notice / rule / equipment / custom
    question_type = Column(String(50), nullable=True)

    # 排序
    sort_order = Column(Integer, default=0)

    # 顯示抑或隱藏
    is_enabled = Column(Boolean, default=True)

    # 可擴充資訊（例如：icon、樣式配置、自訂 metadata）
    config = Column(JSONB, default=lambda: {})

    # Relationship
    event = relationship(
        "Event",
        back_populates="questions",
        lazy="selectin"
    )
