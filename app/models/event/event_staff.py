# app/models/event/event_staff.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventStaff(BaseModel, Base):
    """
    活動工作人員 / 講師 / 領隊 / 志工
    """

    __tablename__ = "event_staffs"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 可選：關聯到 User（若該工作人員有登入系統）
    # 若活動邀請外部講師，無需綁 user_uuid
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # ---------------------------------------------------------
    # 工作人員基本資料
    # ---------------------------------------------------------
    name = Column(String(255), nullable=False)     # 若無 user_uuid，仍需姓名
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    # 職務（leader / assistant / staff / speaker / medical…）
    role = Column(String(100), nullable=False, index=True)

    # 職務說明（負責工作內容）
    description = Column(String, nullable=True)

    # 排序（名單順序）
    sort_order = Column(Integer, default=0)

    # 是否啟用
    is_enabled = Column(Boolean, default=True)

    # 可擴充欄位（分組、站點、裝備配置、權限等）
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="staffs",
        lazy="selectin"
    )

    user = relationship(
        "User",
        lazy="selectin"
    )
