# app/models/activity/activity_template_field.py

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
    from app.models.activity.activity_template_field_option import ActivityTemplateFieldOption
# ---------------------------------------------------------

class ActivityTemplateField(BaseModel, Base):
    __tablename__ = "activity_template_fields"

    # ---------------------------------------------------------
    # 外鍵：ActivityTemplate
    # ---------------------------------------------------------
    template_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("activity_templates.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 欄位基本資訊
    # ---------------------------------------------------------
    field_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    placeholder: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    field_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ---------------------------------------------------------
    # 驗證 / 設定
    # ---------------------------------------------------------
    validation: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # 狀態 / 排序
    # ---------------------------------------------------------
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    template: Mapped["ActivityTemplate"] = relationship(
        "ActivityTemplate",
        back_populates="fields",
        lazy="selectin",
    )

    options: Mapped[list["ActivityTemplateFieldOption"]] = relationship(
        "ActivityTemplateFieldOption",
        back_populates="field",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
