# app/models/activity/activity_template_field_option.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class ActivityTemplateFieldOption(BaseModel, Base):
    __tablename__ = "activity_template_field_options"

    # -----------------------------
    # Foreign Key → TemplateField
    # -----------------------------
    field_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_template_fields.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # -----------------------------
    # Option Data
    # -----------------------------
    label = Column(String(255), nullable=False)    # 顯示文字，例如：男性、女性、其他
    value = Column(String(255), nullable=True)     # 表單提交使用，ex: "M" / "F"
    description = Column(String(500), nullable=True)
    color = Column(String(50), nullable=True)      # 可選：提供色碼
    icon = Column(String(255), nullable=True)      # 可選：icon 名稱

    sort_order = Column(Integer, default=0)        # 排序（越小越前）
    is_enabled = Column(Boolean, default=True)     # 用於前台是否顯示此選項

    # JSON 設定（可擴充，例如：子選項、層級、條件顯示）
    config = Column(JSONB, default=lambda: {})

    # -----------------------------
    # Relationship
    # -----------------------------
    field = relationship(
        "ActivityTemplateField",
        back_populates="options_rel",
        lazy="selectin"
    )
