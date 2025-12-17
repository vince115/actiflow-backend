# app/api/system/me.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.schemas.user.user_response import UserResponse

router = APIRouter(
    prefix="/system/me",
    tags=["System - Me"],
)


@router.get("/", response_model=UserResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    """
    取得目前登入使用者（system scope）
    """
    return identity