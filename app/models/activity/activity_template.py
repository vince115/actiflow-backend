# app/models/activity/activity_template.py

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
    from app.models.activity.activity_type import ActivityType
    from app.models.activity.activity_template_rule import ActivityTemplateRule
    from app.models.activity.activity_template_field import ActivityTemplateField
# ---------------------------------------------------------

class ActivityTemplate(BaseModel, Base):
    __tablename__ = "activity_templates"

    # ---------------------------------------------------------
    # 外部模板代碼（後台 / 報表用）
    # ---------------------------------------------------------
    template_code: Mapped[Optional[str]] = mapped_column(
        String,
        unique=True,
        nullable=True,
        index=True,
    )


    # ---------------------------------------------------------
    # 外鍵：組織
    # ---------------------------------------------------------
    organizer_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 外鍵：活動類型
    # ---------------------------------------------------------
    activity_type_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("activity_types.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 基本資料
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # 模板排序
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=100,
    )

    # 表單 / 樣式 / 欄位排序等設定
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    # 一個模板對多個活動
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="activity_template",
        lazy="selectin",
    )

    # 多對一（模板 → 活動類型）
    activity_type: Mapped["ActivityType"] = relationship(
        "ActivityType",
        back_populates="templates",
        lazy="selectin",
    )

    # 一個 template 對多個 ActivityTemplateRule（關聯表/橋接表）
    rules: Mapped[List["ActivityTemplateRule"]] = relationship(
        "ActivityTemplateRule",
        back_populates="template",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # 一個模板對多個欄位
    fields: Mapped[list["ActivityTemplateField"]] = relationship(
        "ActivityTemplateField",
        back_populates="template",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
