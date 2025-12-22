# app/schemas/event/core/organizer/organizer_event_create.py

from app.schemas.event.core.organizer.organizer_event_base import OrganizerEventBase


class OrganizerEventCreate(OrganizerEventBase):
    """
    Organizer scoped Event Create schema

    - organizer_uuid：由 require_current_organizer_admin 注入
    - event_code：由後端產生
    """
    pass
