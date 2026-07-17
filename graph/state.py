from typing import TypedDict

class MatchState(TypedDict):
    job_url: str
    job_title: str
    job_description: str

    cv_data: dict
    job_data: dict

    analysis: dict