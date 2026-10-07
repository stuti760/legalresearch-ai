from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
# bge models expect this prefix on search queries (not on the passages themselves)
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_passages(texts: list[str]) -> list[list[float]]:
    vectors = get_model().encode(texts, batch_size=16, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    vector = get_model().encode(QUERY_PREFIX + text, normalize_embeddings=True)
    return vector.tolist()


def to_pgvector(vector: list[float]) -> str:
    """Format a vector the way Postgres expects: '[0.1,0.2,...]'."""
    return "[" + ",".join(f"{x:.6f}" for x in vector) + "]"