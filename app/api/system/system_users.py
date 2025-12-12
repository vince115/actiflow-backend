# app/api/system/system_users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin
from app.schemas.user.user import UserResponse, UserUpdate
from crud.user.user import (
    list_users,
    get_user_by_uuid,
    update_user,
    soft_delete_user,
)

router = APIRouter(prefix="/system/users", tags=["System Users"])


# -----------------------------------------------------------
# 取得所有使用者
# -----------------------------------------------------------
@router.get("/", response_model=list[UserResponse])
def fetch_users(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_super_admin),
):
    return list_users(db)


# -----------------------------------------------------------
# 查看單一使用者
# -----------------------------------------------------------
@router.get("/{user_uuid}", response_model=UserResponse)
def fetch_user(
    user_uuid: str,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_super_admin),
):
    user = get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(404, "User not found")
    return user


# -----------------------------------------------------------
# 更新使用者（後台）
# -----------------------------------------------------------
@router.put("/{user_uuid}", response_model=UserResponse)
def update_user_detail(
    user_uuid: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_super_admin),
):
    updated = update_user(db, user_uuid, data)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated


# -----------------------------------------------------------
# 刪除使用者（假刪除）
# -----------------------------------------------------------
@router.delete("/{user_uuid}")
def remove_user(
    user_uuid: str,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_super_admin),
):
    deleted = soft_delete_user(db, user_uuid)
    if not deleted:
        raise HTTPException(404, "User not found")

    return {"message": "User deleted"}
