import re

from psycopg.rows import dict_row

from app.db import get_conn

SQL = """
SELECT id AS chunk_id, case_name, court, year, area, page, issue, content,
       ts_rank(tsv, query) AS score
FROM chunks, to_tsquery('english', %(q)s) AS query
WHERE tsv @@ query
  AND (%(area)s::text IS NULL OR area = %(area)s)
  AND (%(issue)s::text IS NULL OR %(issue)s = ANY(issue))
ORDER BY score DESC
LIMIT %(limit)s
"""


def build_or_query(text: str) -> str:
    """'what is desertion' -> 'what | desertion' (letters and digits only, so it's safe)."""
    words = re.findall(r"[a-z0-9]{3,}", text.lower())
    return " | ".join(dict.fromkeys(words))  # unique words, original order


def fulltext_search(
    query: str, limit: int, area: str | None = None, issue: str | None = None
) -> list[dict]:
    q = build_or_query(query)
    if not q:
        return []
    params = {"q": q, "area": area, "issue": issue, "limit": limit}
    with get_conn() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(SQL, params)
        return cur.fetchall()