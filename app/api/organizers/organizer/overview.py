# app/api/organizers/organizer/overview.py

from fastapi import APIRouter

from app.api.organizers.organizer.dashboard import router as dashboard_router
from app.api.organizers.organizer.events import router as events_router
from app.api.organizers.organizer.applications import router as applications_router
from app.api.organizers.organizer.members import router as members_router

router = APIRouter()

router.include_router(dashboard_router)
router.include_router(events_router)
router.include_router(applications_router)
# router.include_router(members_router) # members.py seems empty/incomplete based on previous check, so commenting out for now to avoid errors if it's not ready.
