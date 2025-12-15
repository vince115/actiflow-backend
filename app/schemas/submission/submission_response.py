# app/schemas/submission/submission_response.py

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from app.schemas.submission.submission_base import SubmissionBase
from app.schemas.submission.submission_value import SubmissionValueResponse


class SubmissionResponse(SubmissionBase):
    """
    Organizer / Admin 後台最終回傳的 Submission 資料格式
    - 繼承 SubmissionBase（保留所有共用欄位）
    - 加上 values（submission values）
    - 加上 JOIN user 資訊
    """

    uuid: UUID

    # JOIN User 資訊（後台需要）
    user_name: Optional[str] = None
    user_email: Optional[str] = None   # 覆蓋 base，是 OK 的（相同欄位 Pydantic 會合併）

    # 每一筆 submission 對應的欄位值
    values: List[SubmissionValueResponse] = []

    model_config = {"from_attributes": True}
