import csv
import json
from pathlib import Path

from app.ingestion.chunker import chunk_paragraphs
from app.ingestion.pdf_text import extract_paragraphs

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def main() -> None:
    with open(DATA_DIR / "metadata.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = 0
    with open(DATA_DIR / "chunks.jsonl", "w", encoding="utf-8") as out:
        for row in rows:
            pdf_path = DATA_DIR / "pdfs" / row["filename"]
            if not pdf_path.exists():
                print(f"MISSING FILE: {row['filename']}")
                continue

            chunks = chunk_paragraphs(extract_paragraphs(pdf_path))
            if not chunks:
                print(f"NO TEXT (scanned PDF?): {row['filename']}")
                continue

            for i, chunk in enumerate(chunks):
                record = {
                    "case_name": row["case_name"],
                    "court": row["court"],
                    "year": int(row["year"]),
                    "area": row["area"],
                    "page": chunk["page"],
                    "chunk_index": i,
                    "content": chunk["content"],
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

            sizes = [len(c["content"].split()) for c in chunks]
            print(
                f"{row['case_name']}: {len(chunks)} chunks, words "
                f"min/avg/max = {min(sizes)}/{sum(sizes) // len(sizes)}/{max(sizes)}"
            )
            total += len(chunks)

    print(f"Total chunks: {total}")


if __name__ == "__main__":
    main()