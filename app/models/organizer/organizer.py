# app/models/organizer/organizer.py

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class Organizer(BaseModel, Base):
    """
    活動主辦單位（Organizer）
    - 企業級設計：id + uuid
    - organizer_uuid 為業務代碼
    """
    __tablename__ = "organizers"

    # （active/not active）會結束營運/會停用/或不想讓舊活動仍歸屬於此主辦者
    status = Column(
        String,
        default="pending",   # pending / approved / rejected
        nullable=False,
        index=True
    )

    # 公司資料（不是帳號）
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(JSONB, nullable=True)
    website = Column(String, nullable=True)
    description = Column(String, nullable=True)

    # LOGO / Banner 
    logo_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)

    # 企業設定
    config = Column(JSONB, default=lambda: {})

    # Relationship
    memberships = relationship(
        "OrganizerMembership",
        back_populates="organizer",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    users = relationship(
        "User", 
        secondary="organizer_memberships", 
        viewonly=True,
        lazy="selectin"
    )

    events = relationship(
        "Event",
        back_populates="organizer",
        lazy="selectin"
    )
    
