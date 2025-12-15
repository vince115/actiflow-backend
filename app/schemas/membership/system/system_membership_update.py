# app/schemas/membership/system_membership_update.py

from pydantic import BaseModel
from typing import Optional

class SystemMembershipUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None

    model_config = {"from_attributes": True}
