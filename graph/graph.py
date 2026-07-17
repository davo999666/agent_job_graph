from langgraph.graph import StateGraph, END

from graph.routers import route_cv_cache

from graph.state import MatchState
from graph.nodes import ( check_cv_cache, extract_cv, extract_job, match )

builder = StateGraph(MatchState)

builder.add_node("check_cv_cache", check_cv_cache)
builder.add_node("extract_cv", extract_cv)
builder.add_node("extract_job", extract_job)
builder.add_node("match", match)

builder.set_entry_point("check_cv_cache")

builder.add_conditional_edges(
    "check_cv_cache",
    route_cv_cache,
)

builder.add_edge("extract_cv", "extract_job")
builder.add_edge("extract_job", "match")
builder.add_edge("match", END)

graph = builder.compile()



