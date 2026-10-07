import json
from pathlib import Path


from app.db import get_conn
from app.ingestion.tagger import tag_issues
from app.retrieval.embeddings import embed_passages, to_pgvector

CHUNKS_FILE = Path(__file__).resolve().parents[2] / "data" / "chunks.jsonl"

INSERT_SQL = """
INSERT INTO chunks (case_name, court, year, area, page, chunk_index, content, embedding, issue)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector, %s::text[])
"""


def main() -> None:
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        records = [json.loads(line) for line in f]
    print(f"Embedding {len(records)} chunks (first run downloads the model)...")

    vectors = embed_passages([r["content"] for r in records])

    rows = [
        (
            r["case_name"], r["court"], r["year"], r["area"],
             r["page"], r["chunk_index"], r["content"], to_pgvector(v),
            tag_issues(r["content"], r["area"]),
        )
        for r, v in zip(records, vectors)
    ]

    with get_conn() as conn:
        conn.execute("TRUNCATE chunks RESTART IDENTITY")
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, rows)
    print(f"Loaded {len(rows)} chunks into the database.")


if __name__ == "__main__":
    main()