# app/schemas/common/pagination.py  ← 分頁回傳格式

from pydantic import BaseModel
from typing import List, Any


class PaginatedResponse(BaseModel):
    """
    通用分頁回傳格式（簡化版）

    - total: 總筆數
    - page: 當前頁
    - page_size: 每頁筆數
    - items: 資料列表（由 response_model 決定內容）
    """

    total: int
    page: int
    page_size: int
    items: List[Any]

    model_config = {"from_attributes": True}
    