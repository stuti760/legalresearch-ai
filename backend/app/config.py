import os
from pathlib import Path

from dotenv import load_dotenv
from psycopg.conninfo import make_conninfo

# .env lives in the project root, three levels up from this file
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def get_db_dsn() -> str:
    return make_conninfo(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
    )