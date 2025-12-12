# app/models/event/event_field.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventField(BaseModel, Base):
    """
    活動複製自模板的欄位（最終報名表單）
    """
    __tablename__ = "event_fields"

    # ---------------------------------------------------------
    # 外鍵：Event
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 基本欄位資訊（從 Template 複製）
    # ---------------------------------------------------------
    field_key = Column(String(100), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    placeholder = Column(String(255), nullable=True)
    description = Column(String, nullable=True)

    field_type = Column(String(50), nullable=False)
    required = Column(Boolean, default=False)

    sort_order = Column(Integer, default=0)

    # 選項（若未拆為 Option Model）
    options = Column(JSONB, default=lambda: [])

    # 欄位設定
    config = Column(JSONB, default=lambda: {})

    # 驗證規則（min/max/regex/file_size...）
    validation = Column(JSONB, default=lambda: {})

    # 啟用 / 停用
    is_enabled = Column(Boolean, default=True)

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="fields",
        lazy="selectin",
    )

