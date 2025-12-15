# app/schemas/membership/organizer_membership_public.py

from pydantic import BaseModel

class OrganizerMembershipPublic(BaseModel):
    organizer_uuid: str
    organizer_name: str
    membership_role: str    # owner / admin / editor / viewer / member
    status: str             # active / suspended

    model_config = {"from_attributes": True}
