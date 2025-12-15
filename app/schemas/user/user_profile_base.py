# app/schemas/user/user_profile_base.py

from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserProfileBase(BaseModel):
    """
    UserProfile 基底（internal / response 共用）
    """

    birthday: Optional[date] = None
    address: Optional[dict] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
