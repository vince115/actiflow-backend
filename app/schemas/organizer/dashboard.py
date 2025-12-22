# app/schemas/organizer/dashboard.py

from pydantic import BaseModel
from uuid import UUID


class OrganizerDashboardStats(BaseModel):
    members_count: int
    events_count: int
    active_events: int
    submissions_last_7_days: int


class OrganizerDashboardResponse(BaseModel):
    organizer_uuid: UUID
    organizer_name: str
    stats: OrganizerDashboardStats
