# app/models/event_field.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base_model import BaseModel
from app.schemas.event_field import EventFieldCreate, EventFieldUpdate

class EventField(BaseModel, Base):
    """
    活動的自訂欄位（textfield、select、file...）
    - 對應報名表單的欄位
    """
    __tablename__ = "event_fields"

    # PK 來自 BaseModel：uuid

    # 業務欄位代號（例如 email / phone / team_name）
    field_key = Column(String, nullable=False, index=True)

    # 外鍵：所屬活動 event
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 欄位顯示設定
    label = Column(String, nullable=False)
    # 欄位型別：text / email / number / select / checkbox / file …
    field_type = Column(String, nullable=False) 
    # placeholder 或預設值
    placeholder = Column(String, nullable=True)
    # 必填？
    required = Column(Boolean, default=False)
    # 排序
    sort_order = Column(Integer, default=0)

    # 選項（select / checkbox / radio）
    options = Column(JSONB, default=list)          # list
    # 更多設定（建議使用 dict）
    config = Column(JSONB, default=dict)           # dict ← 修正！

    # 關聯：一個 Event 有多個欄位
    event = relationship(
        "Event",
        back_populates="fields",
        lazy="selectin"
    )
    # 關聯：一個欄位對應多筆 SubmissionValue
    submission_values = relationship(
        "SubmissionValue",
        back_populates="field",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("event_uuid", "field_key", name="uix_event_field"),
    )
