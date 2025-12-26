# app/crud/submission/crud_submission_status.py

from app.exceptions.submission import InvalidSubmissionStatusTransition

ALLOWED_TRANSITIONS = {

    # Public flow
    "pending": ["email_verified"],
    "email_verified": ["paid"],

    # Organizer decision
    "paid": ["completed", "rejected"],

    # Organizer reopen (undo decision)
    "completed": ["paid"],
    "rejected": ["paid"],
}

def assert_status_transition(
    *,
    current: str,
    target: str,
):
    if target not in ALLOWED_TRANSITIONS.get(current, []):
        raise InvalidSubmissionStatusTransition(
            f"Cannot transition from {current} to {target}"
        )