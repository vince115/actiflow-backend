# app/schemas/common.py

from pydantic import BaseModel
from typing import Optional


class DeleteResponse(BaseModel):
    success: bool = True
    uuid: Optional[str] = None
    message: str = "Deleted successfully"


class StatusMessage(BaseModel):
    success: bool = True
    message: str
