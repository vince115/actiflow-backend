# app/schemas/event/core/event_status_update.py

from pydantic import BaseModel, Field
from typing import Literal


# 你如果已經有統一的 EventStatus enum/常數，這裡改成 import 即可
EventStatus = Literal["draft", "published", "closed", "archived"]


class EventStatusUpdate(BaseModel):
    """
    Admin 專用：更新 Event 狀態的 request body
    """
    status: EventStatus = Field(..., description="New event status")
