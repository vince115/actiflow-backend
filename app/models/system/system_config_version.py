# app/models/system/system_config_version.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class SystemConfigVersion(BaseModel, Base):
    """
    系統設定版本（versioning for SystemSettings / Platform settings）
    - 和 Event 無關
    - 不需要子表
    """

    __tablename__ = "system_config_versions"

    # 顯示代碼（例如：CFG-20250101-001）
    version_code = Column(String, unique=True, nullable=False, index=True)

    # 哪個設定的版本（目標模型）
    target_type = Column(String, nullable=False)  
    # ex: "SystemSettings", "Platform"

    target_uuid = Column(UUID(as_uuid=True), nullable=True)

    # 操作者
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True
    )

    user_email = Column(String, nullable=True)

    # 設定快照（完整內容）
    config_snapshot = Column(JSONB, nullable=False)

    # 安全資訊
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
