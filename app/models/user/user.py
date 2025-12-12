# app/models/user/user.py

from sqlalchemy import Column, String, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class User(BaseModel, Base):

    __tablename__ = "users"

    # 基本資訊
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    avatar_url = Column(String, nullable=True)

    # 個人資訊
    birthday = Column(Date, nullable=True)
    address = Column(JSONB, nullable=True)
    school = Column(String, nullable=True)
    employment = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)

    # 登入資訊
    auth_provider = Column(String, default="local", nullable=False)
    provider_id = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)

    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)

    # 狀態（BaseModel 已提供 is_active / is_deleted）
    last_login_at = Column(DateTime, nullable=True)

    # 使用者設定
    config = Column(JSONB, default=lambda: {})

    # 平台層級角色（新的 RBAC 設計）
    system_membership = relationship(
        "SystemMembership",
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )

    # Organizer 層級 Membership（多對多）
    memberships = relationship(
        "OrganizerMembership",
        back_populates="user",
        lazy="selectin"
    )

    organizers = relationship(
        "Organizer",
        secondary="organizer_memberships",
        viewonly=True,
        lazy="selectin"
    )

    submissions = relationship(
        "Submission",
        back_populates="user",
        lazy="selectin"
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    email_verifications = relationship(
        "EmailVerification",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    password_resets = relationship(
        "PasswordReset",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    sessions = relationship(
        "UserSession",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )