# app/schemas/user/user_profile_create.py

from pydantic import BaseModel
from typing import Optional


class UserProfileCreate(BaseModel):
    user_uuid: str
    birthday: Optional[str] = None
    address: Optional[str] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None
