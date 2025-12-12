# app/models/file/file.py

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.models.base.base_model import BaseModel


class File(BaseModel, Base):
    """
    企業級 File Storage
    """
    __tablename__ = "files"

    url = Column(String, nullable=False)
    name = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    size_bytes = Column(Integer, nullable=True)

    # relationship: many SubmissionFile rows may reference this
    submissions = relationship(
        "SubmissionFile",
        back_populates="file",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
