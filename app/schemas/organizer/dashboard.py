from pydantic import BaseModel
from typing import List

from app.schemas.event.event import EventResponse
from app.schemas.organizer_application.organizer_application_response import OrganizerApplicationResponse


class DashboardResponse(BaseModel):
    events_count: int
    members_count: int
    pending_applications_count: int
    
    recent_events: List[EventResponse]
    recent_applications: List[OrganizerApplicationResponse]
