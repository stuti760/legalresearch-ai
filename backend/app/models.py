from pydantic import BaseModel


class Passage(BaseModel):
    chunk_id: int
    case_name: str
    court: str
    year: int
    area: str
    page: int
    issue: list[str]
    content: str
    score: float
    citation: str


class SearchResponse(BaseModel):
    query: str
    mode: str
    results: list[Passage]