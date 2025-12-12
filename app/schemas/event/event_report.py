# app/schemas/event/event_report.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from app.schemas.base.base_model import BaseSchema


class EventReportResponse(BaseSchema):
    event_uuid: UUID
    total_submissions: int
    total_income: Optional[float] = None
    summary_json: Dict[str, Any] = {}

    model_config = {"from_attributes": True}