# app/api/utils/submission_code.py

from datetime import datetime

def generate_submission_code(event_code: str) -> str:
    """
    Example: EVT-20251224-001
    """
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{event_code}-{ts}"
