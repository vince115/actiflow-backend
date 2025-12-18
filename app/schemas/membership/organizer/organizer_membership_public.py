# app/schemas/membership/organizer_membership_public.py

from typing import Literal
from app.schemas.membership.membership_base import MembershipBase

class OrganizerMembershipPublic(MembershipBase):
    type: Literal["organizer"] = "organizer"

    organizer_uuid: str
    organizer_name: str

    membership_role: str    # owner / admin / editor / viewer / member
