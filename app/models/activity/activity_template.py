# app/models/activity/activity_template.py

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class ActivityTemplate(BaseModel, Base):
    __tablename__ = "activity_templates"

    # 建議加入外部編號（可選）
    # 如： TPL-2025-001，用於後台管理/報表
    template_code = Column(String, unique=True, nullable=True, index=True)

    # 外鍵：用 uuid 串 activity_types
    activity_type_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_types.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 基本資料
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # 模板排序（可調整順序）
    sort_order = Column(Integer, default=100)

    # JSONB：表單設定、樣式、自訂欄位順序等
    config = Column(JSONB, default=lambda: {})

    # Relationship：一個模板對多個欄位
    fields = relationship(
        "TemplateField",
        back_populates="template",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Relationship：多對一（模板 → 活動類型）
    activity_type = relationship(
        "ActivityType",
        back_populates="templates",
        lazy="selectin"
    )

    # Relationship：一個模板對多個活動
    events = relationship(
    "Event",
    back_populates="activity_template",
    lazy="selectin"
)

