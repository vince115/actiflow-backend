# app/models/membership/organizer_membership.py

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


ORGANIZER_ROLES = (
    "owner",
    "admin",
    "editor",
    "viewer",
    "member",
)


class OrganizerMembership(BaseModel, Base):
    """
    使用者加入主辦單位的 Membership（多對多）
    - 一個 user 可以加入多個 organizer
    - 每個 organizer 內只能有一種角色
    """

    __tablename__ = "organizer_memberships"

    __table_args__ = (
        UniqueConstraint("user_uuid", "organizer_uuid", name="uq_user_organizer"),
    )

    # ---------------------------------------------------------
    # 外鍵
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    organizer_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 組織內角色
    # ---------------------------------------------------------
    role = Column(String, nullable=False, index=True, default="member")

    # ---------------------------------------------------------
    # 成員狀態（非資料列 is_active）
    # ---------------------------------------------------------
    is_suspended = Column(Boolean, default=False)
    suspended_reason = Column(String, nullable=True)

    # ---------------------------------------------------------
    # 可擴充資料（例如：限定可管理哪些 event）
    # ---------------------------------------------------------
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # 關聯
    # ---------------------------------------------------------
    user = relationship("User", back_populates="memberships", lazy="selectin")
    organizer = relationship("Organizer", back_populates="memberships", lazy="selectin")