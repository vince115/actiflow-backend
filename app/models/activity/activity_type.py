# app/models/activity/activity_type.py
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class ActivityType(BaseModel, Base):
    __tablename__ = "activity_types"

    # 唯一 KEY（不可重複）
    category_key = Column(String, unique=True, nullable=False, index=True)

    # 顯示名稱
    label = Column(String, nullable=False)

    # 分組（可選，用於大型平台分類）
    group = Column(String, nullable=True)

    # 簡介（可選）
    description = Column(Text, nullable=True)

    # UI 標籤色
    color = Column(String, nullable=True)

    # Heroicons / SVG 名稱
    icon = Column(String, nullable=True)

    # 排序
    sort_order = Column(Integer, default=100)

    # 額外彈性設定
    config = Column(JSONB, default=lambda: {})

    # 是否啟用
    is_enabled = Column(Boolean, default=True)

    # 一種類型對多個模板
    templates = relationship(
        "ActivityTemplate",
        back_populates="activity_type",
        lazy="selectin"
    )
