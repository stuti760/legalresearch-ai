import re
from pathlib import Path

import pymupdf

MIN_BLOCK_WORDS = 4  # shorter blocks are usually page numbers
HEADER = re.compile(
    r"https?://JUDIS\.NIC\.IN\s+SUPREME\s+COURT\s+OF\s+INDIA\s+Page\s+\d+\s+of\s+\d+",
    re.IGNORECASE,
)

# whole-block junk: page labels, Indian Kanoon headers and footers, citation lists
JUNK_BLOCKS = [
    re.compile(r"Page \d+ of \d+"),
    re.compile(r"Indian Kanoon - https?://\S+ ?\d*"),
    re.compile(r".{5,120} on \d{1,2} \w+, \d{4}"),
    re.compile(r"Equivalent citations:.*"),
]


def clean_block(text: str) -> str:
    text = HEADER.sub("", text)  # remove the website header on each page
    text = text.replace("\u00ad", "")  # soft hyphens
    text = re.sub(r"([a-z])-\n([a-z])", r"\1\2", text)  # re-join split words
    text = re.sub(r"\s+", " ", text).strip()
    return "" if any(p.fullmatch(text) for p in JUNK_BLOCKS) else text


def extract_paragraphs(pdf_path: Path) -> list[tuple[int, str]]:
    """Return (page_number, paragraph_text) pairs, pages counted from 1."""
    paragraphs = []
    with pymupdf.open(pdf_path) as doc:
        for page_no, page in enumerate(doc, start=1):
            for block in page.get_text("blocks", sort=True):
                if block[6] != 0:  # 0 = text block, others are images
                    continue
                text = clean_block(block[4])
                if len(text.split()) >= MIN_BLOCK_WORDS:
                    paragraphs.append((page_no, text))
    return paragraphs