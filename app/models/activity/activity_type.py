# app/models/activity/activity_type.py

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
    from app.models.activity.activity_template import ActivityTemplate
# ---------------------------------------------------------

class ActivityType(BaseModel, Base):
    __tablename__ = "activity_types"

    # ---------------------------------------------------------
    # 唯一分類 KEY（程式 / API 使用）
    # ---------------------------------------------------------
    category_key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 顯示資訊
    # ---------------------------------------------------------
    label: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    group: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # UI 標籤色 / icon
    color: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    icon: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # 排序 / 狀態
    # ---------------------------------------------------------
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=100,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------------------------
    # 彈性設定
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    templates: Mapped[list["ActivityTemplate"]] = relationship(
        "ActivityTemplate",
        back_populates="activity_type",
        lazy="selectin",
    )
