from typing import TypedDict

class State(TypedDict):
    booking_reference: str
    bkg_data: dict
    si_data: dict
    missing_answer: str
    summary_answer: str
    next: str