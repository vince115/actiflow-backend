# app/schemas/organizer_application/organizer_application_create.py

from pydantic import BaseModel
from typing import Optional


class OrganizerApplicationCreate(BaseModel):
    """
    User 發起申請建立新 Organizer。
    user_uuid 由後端從 JWT / auth.me 取得，不由前端傳入。
    """

    name: str
    description: Optional[str] = None
    reason: Optional[str] = None

    model_config = {"from_attributes": True}
