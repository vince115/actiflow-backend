# app/schemas/common/pagination.py  ← 分頁回傳格式

from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    通用分頁回傳格式（Generic 版）

    - total: 總筆數
    - page: 當前頁
    - page_size: 每頁筆數
    - items: 資料列表（型別由 T 決定）
    """

    total: int
    page: int
    page_size: int
    items: List[T]

    model_config = {"from_attributes": True}

    