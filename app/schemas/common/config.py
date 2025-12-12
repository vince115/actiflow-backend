# app/schemas/common/config.py  ← Config 統一格式

from typing import Dict, Any
from pydantic import BaseModel


class ConfigObject(BaseModel):
    """
    通用 config 結構，允許存各種設定（key-value）。
    例如：
    - User.config
    - Organizer.config
    - ActivityTemplate.config
    """

    __root__: Dict[str, Any] = {}

    model_config = {"from_attributes": True}
