from typing import Literal

from fastapi import APIRouter, Query

from app.models import SearchResponse
from app.retrieval.search import search

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
def search_endpoint(
    q: str = Query(..., min_length=3),
    mode: Literal["vector", "hybrid"] = "vector",
    limit: int = Query(5, ge=1, le=20),
    area: Literal["criminal", "property", "divorce"] | None = None,
    issue: Literal["cruelty", "desertion"] | None = None,
) -> dict:
    results = search(q, mode=mode, limit=limit, area=area, issue=issue)
    return {"query": q, "mode": mode, "results": results}