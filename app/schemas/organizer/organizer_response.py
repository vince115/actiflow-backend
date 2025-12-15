# app/schemas/organizer/organizer_response.py

from uuid import UUID
from typing import Optional, Dict, Any
from app.schemas.organizer.organizer_base import OrganizerBase
from app.schemas.common.base import BaseSchema


class OrganizerResponse(OrganizerBase, BaseSchema):
    """
    組織完整回傳資料（給後台管理或內部 API 使用）
    - 具備 BaseSchema（uuid、audit 欄位）
    - 具備 OrganizerBase（基本資料）
    """

    # BaseSchema 已包含 uuid 和 audit 欄位

    model_config = {"from_attributes": True}