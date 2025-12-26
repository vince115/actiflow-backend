# app/exceptions/event.py   

class InvalidEventStatusTransition(Exception):
    """
    Raised when an invalid event status transition is attempted.
    """
    pass