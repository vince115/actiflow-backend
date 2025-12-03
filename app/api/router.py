# app/api/router.py

from fastapi import APIRouter

from app.api.auth.organizer_auth import router as organizer_auth_router
from app.api.auth.super_admin_auth import router as super_admin_auth_router
from app.api.auth.user_auth import router as user_auth_router
from app.api.auth.system_auth import router as user_auth_router


from app.api.activity_types import router as activity_types_router
from app.api.activity_templates import router as activity_templates_router
from app.api.events import router as events_router
from app.api.organizers import router as organizers_router
from app.api.submissions import router as submissions_router

from app.api.organizers import (
    router as admin_organizer_router,
)


api_router = APIRouter()

# Auth Routers
api_router.include_router(organizer_auth_router, prefix="/auth")
api_router.include_router(super_admin_auth_router, prefix="/auth")
api_router.include_router(user_auth_router, prefix="/auth")

# CRUD Routers
api_router.include_router(activity_types_router, prefix="/activity-types", tags=["Activity Types"])
api_router.include_router(activity_templates_router, prefix="/activity-templates", tags=["Activity Templates"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(organizers_router, prefix="/organizers", tags=["Organizers"])
api_router.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])

# ✅ 新增：後台審核 Organizer 的 router
api_router.include_router(
    admin_organizer_router,
    # 如果你的 endpoints_admin_organizer.py 裡面本身 prefix 是 "/admin/organizers"
    # 這裡就不用再加 prefix
    # 如果裡面 prefix 是 ""，你也可以在這裡加 prefix="/admin/organizers"
)