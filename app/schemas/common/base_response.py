# app/schemas/common/base_response.py  ← API Response Wrapper

from pydantic import BaseModel
from typing import Any, Optional


class BaseAPIResponse(BaseModel):
    """
    統一 API 回傳格式（非資料表 Response）。
    實際資料回傳放在 data 欄位。
    """

    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None

    class Config:
        from_attributes = True
