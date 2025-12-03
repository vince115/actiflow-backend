# app/models/activity_type.py

from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db import Base
from app.models.base_model import BaseModel


class ActivityType(BaseModel, Base):
    __tablename__ = "activity_types"

    # 企業代號：不能重複
    category_key = Column(String, unique=True, nullable=False, index=True)

    # 顯示名稱
    label = Column(String, nullable=False)

    # 簡介（可選）
    description = Column(Text, nullable=True)

    # 顏色欄位  ex: "#FF9900"
    color = Column(String, nullable=True)  

    # icon 圖示 （用 Tailwind Heroicons / 或 SVG）
    icon = Column(String, nullable=True)

    # 排序用 weight
    sort_order = Column(Integer, default=100)

    # 彈性設定 (重要: default 要用 lambda)
    config = Column(JSONB, default=lambda: {})

    # Relationship：一種活動類型對多個模板
    templates = relationship("ActivityTemplate", back_populates="activity_type", lazy="selectin")
