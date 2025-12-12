# app/schemas/activity_type/activity_type_create.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ActivityTypeCreate(BaseModel):
    category_key: str
    label: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
