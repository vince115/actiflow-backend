# app/schemas/system_membership/system_membership_response.py

from uuid import UUID
from app.schemas.system_membership.system_membership_base import SystemMembershipBase
from app.schemas.common.base_model import BaseSchema


class SystemMembershipResponse(SystemMembershipBase, BaseSchema):
    """
    回傳平台角色關聯資訊：
    - uuid
    - user_uuid
    - role
    - audit fields
    """

    model_config = {
        "from_attributes": True
    }
