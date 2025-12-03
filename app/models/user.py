# app/models/user.py

from sqlalchemy import  Column, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db import Base
from app.models.base_model import BaseModel


class User(BaseModel, Base):
    
    __tablename__ = "users"

    # 平台角色（與 Organizer 無關）
    # user / super_admin
    role = Column(String, default="user", nullable=False, index=True)
    
    # 基本資料
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    avatar_url = Column(String, nullable=True)

    # 個人資料
    birthday = Column(Date, nullable=True)
    address = Column(JSONB, nullable=True) # JSONB（縣市、區域、郵遞區號、街道）
    school = Column(String, nullable=True)
    employment = Column(String, nullable=True)  # 原本 company → 改更通用
    job_title = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)

    # # OAuth provider ( local / google / facebook / apple / line )
    auth_provider = Column(String, default="local", nullable=False)
    provider_id = Column(String, nullable=True)  # ← 建議補上

    # 密碼（第三方登入可為 None）
    password_hash = Column(String, nullable=True)

    # Email 驗證流程（與 SuperAdmin 相同）
    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)

    # 附加設定（推薦）
    config = Column(JSONB, nullable=True)

    # 多對多：加入的主辦單位（通過 OrganizerMembership）
    memberships = relationship(
        "OrganizerMembership",
        back_populates="user",
        lazy="selectin"
    )

    # 方便使用者直接查詢自己參與的主辦單位
    organizers = relationship(
        "Organizer",
        secondary="organizer_memberships",
        viewonly=True,
        lazy="selectin"
    )

    # 報名資料
    submissions = relationship(
        "Submission",
        back_populates="user",
        lazy="selectin"
    )
