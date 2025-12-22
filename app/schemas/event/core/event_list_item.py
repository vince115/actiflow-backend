# app/schemas/event/core/event_list_item.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.schemas.common.base import BaseSchema


class OrganizerEventListItem(BaseSchema):
    """
    Organizer 後台 Event 列表用（輕量版）
    - 不帶 template/fields 大物件
    - 只回傳列表頁真的需要的欄位
    """

    event_code: str
    name: str
    status: str  # draft / published / closed

    activity_template_uuid: Optional[UUID] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    submissions_count: int = 0

    model_config = {"from_attributes": True}
