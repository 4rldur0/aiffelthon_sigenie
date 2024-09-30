from typing import TypedDict

class State(TypedDict):
    parties_answer: str
    policy_answer: str
    news_answer: str
    summary_answer: str
    si_data: dict
    next: str