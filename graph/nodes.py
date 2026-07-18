import json

from cv_extractor.extractor import ( cache_is_valid, find_cv, load_cached_cv, read_cv, save_cv_cache)
from LangChain.chain import ( job_extract_chain, cv_match_chain, cv_extract_chain)


def check_cv_cache(state):
    cv_file = find_cv()
    cached_data = load_cached_cv() if cache_is_valid(cv_file) else None

    return {
        "cv_data": cached_data,
    }


def extract_cv(state):
    cv_file = find_cv()
    cv_text = read_cv(cv_file)

    cv_data = cv_extract_chain.invoke({
        "cv_text": cv_text,
    })

    if not isinstance(cv_data, dict):
        raise TypeError(
            "cv_extract_chain must return a dictionary."
        )

    save_cv_cache(cv_data)

    return {
        "cv_data": cv_data,
    }


def extract_job(state):
    job_data = job_extract_chain.invoke(
        {
            "job_title": state["job_title"],
            "job_description": state["job_description"],
        }
    )

    if not isinstance(job_data, dict):
        raise TypeError(
            "job_extract_chain must return a dictionary."
        )
    
    with open("data/job_data.json", "w", encoding="utf-8") as f:
        json.dump( job_data, f, ensure_ascii=False, indent=4 )

    return {
        "job_data": job_data,
    }


def match(state):
    analysis = cv_match_chain.invoke(
        {
            "cv_text": json.dumps(
                state["cv_data"],
                ensure_ascii=False,
            ),
            "job_text": json.dumps(
                state["job_data"],
                ensure_ascii=False,
            ),
        }
    )

    if not isinstance(analysis, str):
        raise TypeError(
            "cv_match_chain must return a string."
        )

    return {
        "analysis": analysis,
    }