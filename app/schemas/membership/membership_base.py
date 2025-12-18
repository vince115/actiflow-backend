# app/schemas/membership/membership_base.py

from pydantic import BaseModel
from typing import Literal

class MembershipBase(BaseModel):
    type: Literal["system", "organizer"]

    model_config = {"from_attributes": True}
