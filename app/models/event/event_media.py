# app/models/event/event_media.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventMedia(BaseModel, Base):
    """
    活動媒體資料（圖片 / 附件 / 海報）
    - 封面、輪播圖、PDF 活動簡章、Google Map 圖層、GPX 路線等
    """

    __tablename__ = "event_media"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 媒體類型：image / pdf / file / map / gpx / video
    media_type = Column(String(50), nullable=False, index=True)

    # 媒體 URL（雲端 storage，例如 Cloudflare R2 / GCP / S3）
    url = Column(String(500), nullable=False)

    # 顯示名稱
    title = Column(String(255), nullable=True)

    # 說明文字
    description = Column(String(500), nullable=True)

    # 排序（越小越前）
    sort_order = Column(Integer, default=0)

    # 是否為活動封面
    is_cover = Column(Boolean, default=False)

    # 額外設定（JSONB，可擴充）
    # e.g. {"width": 1200, "height": 800, "gps": {...}, "meta": {...}}
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="media",
        lazy="selectin"
    )
