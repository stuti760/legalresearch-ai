import psycopg

from app.config import get_db_dsn

SCHEMA = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id          SERIAL PRIMARY KEY,
    case_name   TEXT NOT NULL,
    court       TEXT NOT NULL,
    year        INT  NOT NULL,
    area        TEXT NOT NULL,
    page        INT  NOT NULL,
    chunk_index INT  NOT NULL,
    issue       TEXT[] NOT NULL DEFAULT '{}',
    content     TEXT NOT NULL,
    embedding   vector(384),
    tsv         tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

CREATE INDEX IF NOT EXISTS chunks_tsv_idx ON chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_area_idx ON chunks (area);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);
"""


def get_conn() -> psycopg.Connection:
    return psycopg.connect(get_db_dsn())


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(SCHEMA)