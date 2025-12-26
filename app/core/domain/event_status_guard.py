# app/core/domai/event_status_guard.py

"""
Event status transition guard (Domain rule)

說明：
- 定義 Event 狀態「允許的轉換」
- 所有 publish / unpublish / close 都必須經過這裡
- Router / CRUD 不應自行判斷狀態
"""

from fastapi import HTTPException, status

from app.core.constants.event_status import EventStatus


# ---------------------------------------------------------
# Allowed status transitions
# ---------------------------------------------------------
# current_status -> allowed target statuses
ALLOWED_EVENT_STATUS_TRANSITIONS: dict[EventStatus, set[EventStatus]] = {
    EventStatus.DRAFT: {
        EventStatus.PUBLISHED,
    },
    EventStatus.PUBLISHED: {
        EventStatus.DRAFT,     # unpublish
        EventStatus.CLOSED,    # close
    },
    EventStatus.CLOSED: set(),  # terminal state
}


# ---------------------------------------------------------
# Guard function
# ---------------------------------------------------------
def assert_event_status_transition(
    *,
    current: EventStatus,
    target: EventStatus,
) -> None:
    """
    Validate whether an Event status transition is allowed.

    :param current: current EventStatus
    :param target: target EventStatus
    :raises HTTPException: if transition is not allowed
    """

    allowed_targets = ALLOWED_EVENT_STATUS_TRANSITIONS.get(current, set())

    if target not in allowed_targets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Event status cannot transition "
                f"from '{current.value}' to '{target.value}'"
            ),
        )
