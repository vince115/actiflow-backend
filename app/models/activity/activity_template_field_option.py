# app/models/activity/activity_template_field_option.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import Optional, TYPE_CHECKING
from uuid import UUID as PyUUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.activity.activity_template_field import ActivityTemplateField
# ---------------------------------------------------------


class ActivityTemplateFieldOption(BaseModel, Base):
    __tablename__ = "activity_template_field_options"

    # ---------------------------------------------------------
    # Foreign Key → ActivityTemplateField
    # ---------------------------------------------------------
    field_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("activity_template_fields.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Option Data
    # ---------------------------------------------------------
    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    value: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    color: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    icon: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ---------------------------------------------------------
    # JSON Config
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        server_default="{}",
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    field: Mapped["ActivityTemplateField"] = relationship(
        "ActivityTemplateField",
        back_populates="options",
        lazy="selectin",
    )
