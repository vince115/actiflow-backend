# app/schemas/platform/super_admin.py

from pydantic import BaseModel
from uuid import UUID


class SuperAdmin(BaseModel):
    """
    Super Admin 身份資訊（非資料表欄位，不需 audit）
    """

    user_uuid: UUID
    is_super_admin: bool = True

    model_config = {"from_attributes": True}
