# app/schemas/platform/system_membership_response.py

from app.schemas.platform.system_membership_base import SystemMembershipBase
from app.schemas.common.base_model import BaseSchema


class SystemMembershipResponse(SystemMembershipBase, BaseSchema):
    """
    回傳平台層級角色資料
    """

    model_config = {"from_attributes": True}
