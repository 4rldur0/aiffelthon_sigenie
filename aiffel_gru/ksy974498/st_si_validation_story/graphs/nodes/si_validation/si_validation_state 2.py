from typing import TypedDict

class State(TypedDict):
    si_data: dict
    parties_answer: str
    policy_answer: str
    news_answer: str
    summary_answer: str
    next: str