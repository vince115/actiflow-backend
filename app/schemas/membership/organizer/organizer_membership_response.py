# app/schemas/membership/organizer_membership_response.py

from pydantic import BaseModel
from uuid import UUID
from app.schemas.membership.organizer.organizer_membership_base import OrganizerMembershipBase

class OrganizerMembershipResponse(OrganizerMembershipBase):
    uuid: UUID
    organizer_uuid: UUID
    user_uuid: UUID

    model_config = {"from_attributes": True}
