MAX_WORDS = 250
OVERLAP = 30  # words carried from one chunk into the next


def split_long(paragraphs: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Cut any paragraph longer than MAX_WORDS into smaller pieces."""
    pieces = []
    for page, text in paragraphs:
        words = text.split()
        for i in range(0, len(words), MAX_WORDS):
            pieces.append((page, " ".join(words[i : i + MAX_WORDS])))
    return pieces


def chunk_paragraphs(paragraphs: list[tuple[int, str]]) -> list[dict]:
    """Pack whole paragraphs into chunks of up to MAX_WORDS words."""
    chunks = []
    words: list[str] = []
    start_page = last_page = 0
    has_new = False  # True if words holds text not yet saved in a chunk

    for page, text in split_long(paragraphs):
        new_words = text.split()
        if has_new and len(words) + len(new_words) > MAX_WORDS:
            chunks.append({"page": start_page, "content": " ".join(words)})
            words = words[-OVERLAP:]
            start_page, has_new = last_page, False
        if not words:
            start_page = page
        words += new_words
        has_new = True
        last_page = page

    if has_new:
        chunks.append({"page": start_page, "content": " ".join(words)})
    return chunks