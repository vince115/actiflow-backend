# app/models/event/event_media.py

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
# ---------------------------------------------------------

class EventMedia(BaseModel, Base):
    """
    活動媒體資料（圖片 / 附件 / 海報）
    - 封面、輪播圖、PDF 活動簡章、Google Map 圖層、GPX 路線等
    """

    __tablename__ = "event_media"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 媒體資訊
    # ---------------------------------------------------------
    media_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    # 媒體 URL（雲端 storage，例如 Cloudflare R2 / GCP / S3）
    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # 顯示名稱
    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # 說明文字
    description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # 排序（越小越前）
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # 是否為活動封面
    is_cover: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # 額外設定（JSONB，可擴充）
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="media",
        lazy="selectin",
    )
