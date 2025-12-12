# app/api/router.py

from fastapi import APIRouter

# Auth Routers
from app.api.auth.login import router as login_router               # 統一登入 /auth/login
from app.api.auth.refresh import router as refresh_router
from app.api.auth.me import router as me_router
from app.api.auth.logout import router as logout_router

# CRUD Routers
from app.api.activities.activity_types import router as activity_types_router
from app.api.activities.activity_templates import router as activity_templates_router
from app.api.events.events import router as events_router
from app.api.organizers.organizers import router as organizers_router
from app.api.submissions.submissions import router as submissions_router
from app.api.system.organizer_approval import router as organizer_approval_router

api_router = APIRouter()

# -----------------------
# AUTH SECTION
# -----------------------
# 統一登入
api_router.include_router(login_router, prefix="/auth", tags=["Auth"])

# Refresh Token
api_router.include_router(refresh_router, prefix="/auth", tags=["Auth"])

api_router.include_router(me_router, prefix="/auth", tags=["Auth"])
api_router.include_router(logout_router, prefix="/auth", tags=["Auth"])

# -----------------------
# CRUD SECTION
# -----------------------
api_router.include_router(activity_types_router, prefix="/activity-types", tags=["Activity Types"])
api_router.include_router(activity_templates_router, prefix="/activity-templates", tags=["Activity Templates"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(organizers_router, prefix="/organizers", tags=["Organizers"])
api_router.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])

api_router.include_router(organizer_approval_router,prefix="/system/organizer-approval", tags=["System - Organizer Approval"])
