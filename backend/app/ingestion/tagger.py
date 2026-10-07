import re

# Each issue maps to keyword patterns. \b means "whole word boundary".
ISSUE_PATTERNS: dict[str, list[str]] = {
    "cruelty": [
        r"\bcruelty\b",
        r"\bcruel\b",
    ],
    "desertion": [
        r"\bdesertion\b",
        r"\bdeserted\b",
        r"\bdeserts\b",
        r"\banimus deserendi\b",
        r"\b13\s*\(\s*1\s*\)\s*\(\s*ib\s*\)",  # section 13(1)(ib) of the HMA
    ],
}

COMPILED = {
    issue: [re.compile(p, re.IGNORECASE) for p in patterns]
    for issue, patterns in ISSUE_PATTERNS.items()
}


def tag_issues(content: str, area: str) -> list[str]:
    """Return the issues a chunk discusses. Only divorce chunks are tagged."""
    if area != "divorce":
        return []
    return [
        issue
        for issue, patterns in COMPILED.items()
        if any(p.search(content) for p in patterns)
    ]