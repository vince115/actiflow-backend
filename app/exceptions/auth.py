# app/exceptions/base.py

from fastapi import HTTPException
from starlette import status


class ActiFlowException(HTTPException):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=message)


class ActiFlowBusinessException(ActiFlowException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)