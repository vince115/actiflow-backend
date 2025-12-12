# app/models/system/system_audit_log.py

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class SystemAuditLog(BaseModel, Base):
    """
    系統層級操作日誌
    - 用於記錄 super_admin / system_admin 對平台設定的操作
    - 不應該綁定 Event / Submission（那是活動層級）
    """

    __tablename__ = "system_audit_logs"

    # 企業級外部代碼，用來追蹤紀錄
    audit_code = Column(String, unique=True, nullable=False, index=True)

    # 操作者資訊
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    user = relationship("User", lazy="selectin")

    user_email = Column(String, nullable=False, index=True)
    user_role = Column(String, nullable=True)  # super_admin, system_admin, support…

    # 操作類型
    action = Column(
        String,
        nullable=False,
        index=True
    )  # ex: "update_system_settings", "create_platform", "modify_membership"

    # 操作對象（紀錄哪個模型）
    target_type = Column(String, nullable=True)  # ex: "Platform", "SystemSettings", "SystemMembership"
    target_uuid = Column(UUID(as_uuid=True), nullable=True)

    # 操作前後資料快照
    before_data = Column(JSONB, nullable=True)
    after_data = Column(JSONB, nullable=True)

    # 安全資訊
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)

    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # 額外資料
    extra = Column(JSONB, default=lambda: {})