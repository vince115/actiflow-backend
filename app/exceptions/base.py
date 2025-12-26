# app/exceptions/base.py

from fastapi import HTTPException
from starlette import status


class ActiFlowException(HTTPException):
    """
    Base HTTP exception for ActiFlow APIs.

    用途：
    - 僅在 API / router 層使用
    - 將 domain exception 轉為 HTTP response
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(status_code=status_code, detail=message)


class ActiFlowBusinessException(ActiFlowException):
    """
    Business rule violation (4xx)

    語意糖：
    - 預設為 400
    - 可用於狀態衝突、前置條件不符
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, status_code)
