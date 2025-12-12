# app/schemas/platform/system_membership_update.py

from pydantic import BaseModel
from typing import Optional


class SystemMembershipUpdate(BaseModel):
    """
    更新系統層級角色，例如：
    - 停用角色
    - 修改角色權限
    """

    role: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}
