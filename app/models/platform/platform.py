# app/models/platform/platform.py  - 平台 CRUD（super admin 專用）

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class Platform(BaseModel, Base):
    """
    ActiFlow 多平台架構
    - 當前僅使用 1 個平台（ActiFlow）
    - 未來可無痛擴充成多平台（像 Meetup / Shopify 多分站）
    """

    __tablename__ = "platforms"

    # 平台名稱（例：ActiFlow、Meetup Taipei、Photography Platform）
    name = Column(String, nullable=False, index=True)

    # URL slug → /platform/<slug>
    slug = Column(String, nullable=True, unique=True, index=True)

    # 平台域名（可選）
    domain = Column(String, nullable=True, unique=True)

    # 地區代碼（可選）
    region = Column(String, nullable=True)

    # 平台描述
    description = Column(String, nullable=True)

    # 平台啟用狀態
    # active    → 正常
    # suspended → 暫停
    # archived  → 封存
    status = Column(String, nullable=False, default="active")

    # 是否為系統預設平台
    is_default = Column(Boolean, default=False)

    # 平台自訂設定（外觀、Logo、Email 與 SEO 設定等）
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship：Platform ↔ SystemMembership（平台層級角色）
    # ---------------------------------------------------------
    memberships = relationship(
        "SystemMembership",
        back_populates="platform",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
