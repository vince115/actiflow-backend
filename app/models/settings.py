from sqlalchemy import Column, Integer, String, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.core.db import Base


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    site_name = Column(String(255), default="ActiFlow")
    logo_url = Column(String(500), nullable=True)
    support_email = Column(String(255), nullable=True)

    # 系統設定用 JSON
    config = Column(JSON, default={})

    # 啟用 / 刪除
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(
        func.now(),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
