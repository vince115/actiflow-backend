# app/schemas/organizer_application/organizer_application_response.py

from app.schemas.organizer_application.organizer_application_base import OrganizerApplicationBase
from app.schemas.common.base_model import BaseSchema


class OrganizerApplicationResponse(OrganizerApplicationBase, BaseSchema):
    """
    回傳 Organizer Application 完整資訊：
    - BaseSchema: uuid + audit 欄位
    - OrganizerApplicationBase: 申請資料
    """

    model_config = {"from_attributes": True}
