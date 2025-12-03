# app/models/system_membership.py

from sqlalchemy import Column, String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
from app.models.base_model import BaseModel

class SystemMembership(BaseModel, Base):
    """
    User 的平台層級權限（非 Organizer）
    """

    __tablename__ = "system_memberships"

    __table_args__ = (
        UniqueConstraint("user_uuid", name="uq_system_user"),
    )

    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role = Column(
        Enum("system_admin", "site_admin", "support", "auditor",
            name="system_roles"),
        nullable=False,
        default="support"
    )

    status = Column(
        Enum("active", "suspended", name="system_status"),
        nullable=False,
        default="active"
    )

    user = relationship("User", back_populates="system_membership")
