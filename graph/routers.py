from pathlib import Path
from typing import Literal

from cv_extractor.extractor import CV_CACHE_FILE
from graph.state import MatchState



def route_cv_cache(state: MatchState) -> Literal["extract_cv", "extract_job"]:
    if CV_CACHE_FILE.exists():
        return "extract_job"

    return "extract_cv"