# app/schemas/event/staff/event_staff_response.py

from app.schemas.common.base import BaseSchema
from app.schemas.event.staff.event_staff_base import EventStaffBase


# ------------------------------------------------------------
# Event Staff Response
# ------------------------------------------------------------
class EventStaffResponse(EventStaffBase, BaseSchema):
    """
    注意繼承順序：
    - EventStaffBase：業務欄位
    - BaseSchema：uuid + audit
    """
    pass
