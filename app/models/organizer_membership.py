# app/models/organizer_membership.py

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base
from app.models.base_model import BaseModel

class OrganizerMembership(BaseModel, Base):
    """
    使用者加入主辦單位的 Membership（多對多連接表）
    - user_uuid → users.uuid
    - organizer_uuid → organizers.uuid
    - role: owner / staff（組織層級）
    """

    __tablename__ = "organizer_memberships"
    
    #每個使用者在同一組織內只能有一個 membership
    __table_args__ = (
        UniqueConstraint("user_uuid", "organizer_uuid", name="uq_user_organizer"),
    )

    # FK
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

    # 組織角色：owner / admin / editor / viewer / member
    role = Column(
        Enum("owner", "admin", "editor", "viewer", "member", name="organizer_member_roles"),
        nullable=False,
        default="member"
    )
    
    # 會員的使用狀態（不等於 is_active）
    status = Column(
        Enum("active", "suspended", name="organizer_member_status"),
        nullable=False,
        default="active"
    )

    # Relationship
    user = relationship("User", back_populates="memberships", lazy="selectin")
    organizer = relationship("Organizer", back_populates="members", lazy="selectin")
