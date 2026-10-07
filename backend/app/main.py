from fastapi import FastAPI

from app.db import get_conn
from app.routers.search import router as search_router

app = FastAPI(title="LegalResearch AI")
app.include_router(search_router)


@app.get("/health")
def health() -> dict:
    with get_conn() as conn:
        row = conn.execute("SELECT count(*) FROM chunks").fetchone()
    return {"status": "ok", "chunks": row[0]}