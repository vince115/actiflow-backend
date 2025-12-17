# app/models/event/event_question.py

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
class EventQuestion(BaseModel, Base):
    """
    活動常見問題（FAQ）、注意事項、說明區塊
    (不屬於表單欄位，純展示用)
    """

    __tablename__ = "event_questions"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 問題內容
    # ---------------------------------------------------------
    question: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # 答案（可長文字）
    answer: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # 類型（faq / notice / rule / equipment / custom）
    question_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # 排序
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # 顯示抑或隱藏
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # 可擴充資訊（icon、樣式、metadata）
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="questions",
        lazy="selectin",
    )
