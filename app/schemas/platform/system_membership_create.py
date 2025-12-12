# app/schemas/platform/system_membership_create.py

from pydantic import BaseModel
from uuid import UUID


class SystemMembershipCreate(BaseModel):
    """
    建立系統層級角色（平台管理員）
    """

    user_uuid: UUID
    role: str                      # super_admin / system_admin / support / auditor

    model_config = {"from_attributes": True}
