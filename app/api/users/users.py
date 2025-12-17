# app/api/users/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.crud.user.crud_user import user_crud
from app.schemas.user.user_update import UserUpdate
from app.schemas.user.user_response import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ------------------------------------------------------------
# 取得自己的 User 本體
# ------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    return identity


# ------------------------------------------------------------
# 更新自己的 User 本體（基本資料）
# ------------------------------------------------------------
@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    updated = user_crud.update(
        db=db,
        db_obj=identity,
        data=data,
    )
    return updated
