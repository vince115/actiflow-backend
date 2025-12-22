# app/core/constants/event_status.py

"""
Event status constants (Domain-level)

說明：
- 僅定義「狀態本身」
- 不包含任何業務邏輯
- 作為整個系統對 Event 狀態的「唯一真相來源」

⚠️ 請勿在此檔案中加入：
- DB logic
- FastAPI dependency
- status transition rule
"""

from enum import Enum


class EventStatus(str, Enum):
    """
    Event lifecycle status
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"

    def __str__(self) -> str:
        # 方便 logging / f-string
        return self.value
