# app/schemas/common/config.py

from typing import Dict, Any
from pydantic import RootModel


class ConfigObject(RootModel[Dict[str, Any]]):
    """
    通用 config 結構，允許存各種設定（key-value）。
    例如：
    - User.config
    - Organizer.config
    - ActivityTemplate.config
    """

    model_config = {"from_attributes": True}
