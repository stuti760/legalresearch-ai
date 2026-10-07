import csv
from pathlib import Path

from app.retrieval.search import search

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
K = 5
MODES = ["vector"]  # Phases 7 and 8 add "hybrid" and "hybrid_rerank"


def load_questions() -> list[dict]:
    with open(DATA_DIR / "eval_questions.csv", encoding="utf-8") as f:
        return [
            {
                "question": r["question"],
                "area": r["area"],
                "expected": set(r["expected_cases"].split("|")),
            }
            for r in csv.DictReader(f)
        ]


def check_names(questions: list[dict]) -> None:
    with open(DATA_DIR / "metadata.csv", encoding="utf-8") as f:
        known = {r["case_name"] for r in csv.DictReader(f)}
    for q in questions:
        for name in q["expected"] - known:
            raise SystemExit(f"Unknown case name in eval file: {name}")


def run(mode: str, use_area: bool, questions: list[dict]):
    recalls, rrs, misses = [], [], []
    for q in questions:
        area = q["area"] if use_area else None
        results = search(q["question"], mode=mode, limit=K, area=area)
        cases = [r["case_name"] for r in results]
        found = q["expected"] & set(cases)
        recalls.append(len(found) / len(q["expected"]))
        rank = next((i for i, c in enumerate(cases, 1) if c in q["expected"]), None)
        rrs.append(1 / rank if rank else 0.0)
        if not found:
            misses.append(q["question"])
    return sum(recalls) / len(recalls), sum(rrs) / len(rrs), misses


def main() -> None:
    questions = load_questions()
    check_names(questions)
    print(f"{len(questions)} questions, top {K} results each\n")
    for mode in MODES:
        for use_area in (False, True):
            recall, mrr, misses = run(mode, use_area, questions)
            label = "yes" if use_area else "no"
            print(f"{mode:<10} area filter: {label:<4} recall@{K} = {recall:.2f}   MRR = {mrr:.2f}")
            for m in misses:
                print(f"     missed completely: {m}")


if __name__ == "__main__":
    main()