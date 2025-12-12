# app/schemas/common/base_model.py  ← Base Schema（ORM Response）

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class BaseSchema(BaseModel):
    """
    通用 Response Schema 基底。
    對應 SQLAlchemy BaseModel（所有資料表共用欄位）：
    - uuid（主鍵）
    - is_active / is_deleted（狀態欄位）
    - created_at / updated_at / deleted_at（時間欄位）
    - created_by / updated_by / deleted_by（操作者）
    - created_by_role / updated_by_role / deleted_by_role（角色屬性）

    所有 Response Schema 必須繼承 BaseSchema，
    除了 Base / Create / Update schemas。
    """

    uuid: UUID

    # 狀態欄位
    is_active: bool = True
    is_deleted: bool = False

    # 稽核欄位
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
