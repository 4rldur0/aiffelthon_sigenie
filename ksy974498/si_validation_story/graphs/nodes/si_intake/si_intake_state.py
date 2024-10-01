from typing import TypedDict

class State(TypedDict):
    missing_answer: str
    summary_answer: str
    booking_reference: str
    si_data: dict
    next: str