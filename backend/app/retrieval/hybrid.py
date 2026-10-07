from app.retrieval.fulltext import fulltext_search
from app.retrieval.vector import vector_search

RRF_K = 60  # damping constant from the original RRF paper
POOL = 20  # candidates taken from each search


def rrf_merge(rankings: list[list[dict]], limit: int) -> list[dict]:
    """Each chunk scores 1/(K + rank) in every list it appears in; scores are added up."""
    scores: dict[int, float] = {}
    rows: dict[int, dict] = {}
    for ranking in rankings:
        for rank, row in enumerate(ranking, start=1):
            cid = row["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1 / (RRF_K + rank)
            rows.setdefault(cid, row)
    best = sorted(scores, key=scores.get, reverse=True)[:limit]
    return [{**rows[cid], "score": scores[cid]} for cid in best]


def hybrid_search(
    query: str, limit: int, area: str | None = None, issue: str | None = None
) -> list[dict]:
    vec = vector_search(query, POOL, area, issue)
    txt = fulltext_search(query, POOL, area, issue)
    return rrf_merge([vec, txt], limit)