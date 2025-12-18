# app/schemas/membership/system_membership_public.py

from typing import Literal
from app.schemas.membership.membership_base import MembershipBase


class SystemMembershipPublic(MembershipBase):
    type: Literal["system"] = "system"
    role: str          # super_admin / staff / auditor / support
    status: str        # active / suspended
