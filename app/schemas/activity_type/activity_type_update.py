# app/schemas/activity_type/activity_type_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ActivityTypeUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
