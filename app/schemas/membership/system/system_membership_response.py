# app/schemas/membership/system_membership_response.py

from pydantic import BaseModel
from uuid import UUID
from app.schemas.membership.system_membership_base import SystemMembershipBase

class SystemMembershipResponse(SystemMembershipBase):
    uuid: UUID
    user_uuid: UUID

    model_config = {"from_attributes": True}
