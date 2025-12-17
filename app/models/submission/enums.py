# app/models/submission/enums.py

import enum

class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    canceled = "canceled"
    completed = "completed"
    waitlist = "waitlist"

