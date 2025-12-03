# app/api/organizers/organizers.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_system_admin,
)

from app.schemas.organizer import (
    OrganizerCreate,
    OrganizerUpdate,
    OrganizerResponse,
)

from app.crud.organizer import (
    create_organizer,
    update_organizer,
    list_organizers,
    get_organizer_by_uuid,
)

router = APIRouter(
    prefix="/organizers",
    tags=["Organizers"],
)

# ============================================================
# 1. 建立 Organizer（⚠ 一般使用者不能直接建立）
#    → System Admin 用的
#    → 使用者使用「申請」流程在 organizer_apply.py
# ============================================================
@router.post("/", response_model=OrganizerResponse)
def create_new_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_system_admin)
):
    organizer = create_organizer(db, data)
    return organizer


# ============================================================
# 2. 讀取單一 Organizer (所有登入者可查看)
# ============================================================
@router.get("/{uuid}", response_model=OrganizerResponse)
def get_single_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)
):
    organizer = get_organizer_by_uuid(db, uuid)
    if not organizer or organizer.is_deleted:
        raise HTTPException(404, "Organizer not found")

    return organizer


# ============================================================
# 3. 查詢所有 Organizer（system_admin 限定）
# ============================================================
@router.get("/", response_model=list[OrganizerResponse])
def list_all_organizers(
    q: str | None = Query(None, description="搜尋名稱"),
    status: str | None = Query(None, description="狀態過濾"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_system_admin)
):
    organizers = list_organizers(db, skip=skip, limit=limit)

    # 搜尋
    if q:
        q_lower = q.lower()
        organizers = [o for o in organizers if o.name and q_lower in o.name.lower()]

    # 狀態過濾
    if status:
        organizers = [o for o in organizers if o.status == status]

    return organizers


# ============================================================
# 4. 修改 Organizer（system_admin 限定）
# ============================================================
@router.put("/{uuid}", response_model=OrganizerResponse)
def update_organizer_detail(
    uuid: str,
    data: OrganizerUpdate,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_system_admin)
):
    organizer = update_organizer(db, uuid, data)

    if not organizer:
        raise HTTPException(404, "Organizer not found")

    return organizer
