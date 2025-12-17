# app/models/system/system_settings.py

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
    from app.models.user.user import User
# ---------------------------------------------------------

class SystemSettings(BaseModel, Base):
    """
    平台級系統設定（僅 super_admin 可修改）
    - 使用 BaseModel.uuid 做唯一識別
    - 系統通常只有一筆設定（未來可擴充版本化）
    """

    __tablename__ = "system_settings"

    # ---------------------------------------------------------
    # 基本設定
    # ---------------------------------------------------------
    site_name: Mapped[str] = mapped_column(
        String(255),
        default="ActiFlow",
    )

    logo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    support_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Config / Flags
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # 設定版本號（配合 SystemConfigVersion 使用）
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )