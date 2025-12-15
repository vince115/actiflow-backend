# app/schemas/membership/system_membership_public.py

from pydantic import BaseModel

class SystemMembershipPublic(BaseModel):
    role: str          # super_admin / staff / auditor / support
    status: str        # active / suspended

    model_config = {"from_attributes": True}
