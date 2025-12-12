# app/schemas/common/pagination.py  ← 分頁回傳格式

from pydantic import BaseModel
from typing import List, Any


class Pagination(BaseModel):
    """
    分頁資料回傳格式：
    - total: 總資料筆數
    - page: 當前頁碼
    - page_size: 單頁筆數
    - items: 當頁資料列表
    """

    total: int
    page: int
    page_size: int
    items: List[Any]

    model_config = {"from_attributes": True}
