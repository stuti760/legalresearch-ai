from app.retrieval.vector import vector_search
from app.retrieval.hybrid import hybrid_search

MODES = ("vector", "hybrid")  # Phase 8 adds "hybrid_rerank"


def make_citation(row: dict) -> str:
    return f"{row['case_name']}, {row['court']}, {row['year']}, p. {row['page']}"


def search(
    query: str,
    mode: str = "vector",
    limit: int = 5,
    area: str | None = None,
    issue: str | None = None,
) -> list[dict]:
        if mode == "vector":
            rows = vector_search(query, limit, area, issue)
        elif mode == "hybrid":
           rows = hybrid_search(query, limit, area, issue)
        else:
           raise ValueError(f"Unknown search mode: {mode}")
        return [{**row, "citation": make_citation(row)} for row in rows]