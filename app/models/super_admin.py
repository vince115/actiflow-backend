# app/models/super_admin.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base_model import BaseModel


class SuperAdmin(BaseModel, Base):
    """
    企業級 SuperAdmin 模型
    使用 BaseModel.uuid 作為唯一 ID
    """    
    __tablename__ = "super_admins"

    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    password_hash = Column(String, nullable=False)

    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
