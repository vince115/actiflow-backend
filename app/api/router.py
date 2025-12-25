# app/api/router.py

from fastapi import APIRouter

# =======================
# Auth
# =======================
from app.api.auth.login import router as login_router
from app.api.auth.refresh import router as refresh_router
from app.api.auth.me import router as me_router
from app.api.auth.logout import router as logout_router
from app.api.email.public import router as email_public_router
# =======================
# Events - Activity (Organizer Admin)
# =======================
from app.api.events.activity.types import router as activity_types_router
from app.api.events.activity.templates import router as activity_templates_router
from app.api.events.activity.template_fields import router as activity_template_fields_router

# =======================
# Events
# =======================
# Super Admin
from app.api.events.admin.events import router as admin_events_router
from app.api.events.admin.templates import router as admin_templates_router
from app.api.events.admin.types import router as admin_types_router

# Organizer
from app.api.events.organizer.events import router as organizer_events_router
from app.api.events.organizer.event_fields import router as organizer_event_fields_router
from app.api.events.organizer.event_staff import router as organizer_event_staff_router
from app.api.events.organizer.submissions import router as organizer_submissions_router

# Public
from app.api.events.public.events import router as public_events_router
from app.api.events.public.event_detail import router as public_event_detail_router
from app.api.events.public.event_schedule import router as public_event_schedule_router
from app.api.events.public.submissions import router as public_submissions_router

# =======================
# Organizers
# =======================
# Public
from app.api.organizers.public.organizers import router as public_organizers_router

# Organizer
from app.api.organizers.organizer.dashboard import router as organizer_dashboard_router
from app.api.organizers.organizer.events import router as organizer_manage_events_router
from app.api.organizers.organizer.members import router as organizer_members_router
from app.api.organizers.organizer.applications import router as organizer_applications_router
from app.api.organizers.organizer.profile import router as organizer_profile_router
from app.api.organizers.organizer.activity_templates import router as organizer_activity_templates_router

# Admin
from app.api.organizers.admin.organizers import router as admin_organizers_router
from app.api.organizers.admin.organizer_members import router as admin_organizer_members_router
from app.api.organizers.admin.organizer_applications import router as admin_organizer_applications_router
from app.api.organizers.organizer.events_list import router as organizer_events_list_router

# =======================
# System
# =======================
from app.api.system.health import router as system_health_router
from app.api.system.me import router as system_me_router
from app.api.system.memberships import router as system_memberships_router
from app.api.system.permissions import router as system_permissions_router
from app.api.system.settings import router as system_settings_router
from app.api.system.organizer_approval import router as organizer_approval_router


api_router = APIRouter()

# =======================
# Auth
# =======================
api_router.include_router(login_router, prefix="/auth", tags=["Auth"])
api_router.include_router(refresh_router, prefix="/auth", tags=["Auth"])
api_router.include_router(me_router, prefix="/auth", tags=["Auth"])
api_router.include_router(logout_router, prefix="/auth", tags=["Auth"])

api_router.include_router(email_public_router, prefix="/public/email", tags=["Email"])

# =======================
# Events - Activity
# =======================
api_router.include_router(activity_types_router)
api_router.include_router(activity_templates_router)
api_router.include_router(activity_template_fields_router)

# =======================
# Events
# =======================
api_router.include_router(admin_events_router)
api_router.include_router(admin_templates_router)
api_router.include_router(admin_types_router)

api_router.include_router(organizer_events_router)
api_router.include_router(organizer_event_fields_router)
api_router.include_router(organizer_event_staff_router)
api_router.include_router(organizer_submissions_router)

api_router.include_router(public_events_router)
api_router.include_router(public_event_detail_router)
api_router.include_router(public_event_schedule_router)
api_router.include_router(public_submissions_router)

# =======================
# Organizers
# =======================
api_router.include_router(public_organizers_router)

# api_router.include_router(organizer_dashboard_router)
api_router.include_router(
    organizer_dashboard_router,
    prefix="/organizers/{organizer_uuid}",
    tags=["Organizer - Dashboard"],
)

api_router.include_router(
    organizer_manage_events_router,
    prefix="/organizers/organizer",
    tags=["Organizer - Events"],
)

# api_router.include_router(organizer_members_router)

api_router.include_router(
    organizer_events_list_router,
    prefix="/organizers/{organizer_uuid}",
    tags=["Organizer - Events List"],
)

api_router.include_router(
    organizer_members_router,
    prefix="/organizers/{organizer_uuid}",
    tags=["Organizer - Members"],
)
api_router.include_router(organizer_applications_router)
api_router.include_router(organizer_profile_router)



api_router.include_router(admin_organizers_router)
api_router.include_router(admin_organizer_members_router)
api_router.include_router(admin_organizer_applications_router)
api_router.include_router(
    organizer_activity_templates_router,
    prefix="/organizers/organizer",
    tags=["Organizer - Activity Templates"],
)

# =======================
# System
# =======================
api_router.include_router(system_health_router, prefix="/system", tags=["System"])
api_router.include_router(system_me_router, prefix="/system", tags=["System"])
api_router.include_router(system_memberships_router, prefix="/system", tags=["System"])
api_router.include_router(system_permissions_router, prefix="/system", tags=["System"])
api_router.include_router(system_settings_router, prefix="/system", tags=["System"])
api_router.include_router(
    organizer_approval_router,
    prefix="/system/organizer-approval",
    tags=["System - Organizer Approval"],
)
