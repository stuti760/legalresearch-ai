from psycopg.rows import dict_row

from app.db import get_conn
from app.retrieval.embeddings import embed_query, to_pgvector

SQL = """
SELECT id AS chunk_id, case_name, court, year, area, page, issue, content,
       1 - (embedding <=> %(vec)s::vector) AS score
FROM chunks
WHERE (%(area)s::text IS NULL OR area = %(area)s)
  AND (%(issue)s::text IS NULL OR %(issue)s = ANY(issue))
ORDER BY embedding <=> %(vec)s::vector
LIMIT %(limit)s
"""


def vector_search(
    query: str, limit: int, area: str | None = None, issue: str | None = None
) -> list[dict]:
    params = {
        "vec": to_pgvector(embed_query(query)),
        "area": area,
        "issue": issue,
        "limit": limit,
    }
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(SQL, params)
        return cur.fetchall()