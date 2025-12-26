# app/exceptions/submission.py

class InvalidSubmissionStatusTransition(Exception):
    """
    Raised when an invalid submission status transition is attempted.
    """
    pass
