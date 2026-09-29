"""Evaluate RAG runs from JSONL: answer metrics + retrieval metrics.

Input: one JSON object per line with
    {"id": ..., "prediction": "...", "answers": ["gold", ...],
     "retrieved": ["pid", ...],            # optional, ranked
     "gold_evidence": ["pid", ...],        # optional
     "num_searches": 3}                    # optional

    python -m ragkit runs/preds.jsonl --k 1 5 10     (from the code/ directory)

Reports EM, F1, cover-EM (gold string contained in prediction), Recall@k,
All@k (every gold passage retrieved; HiKEY's "All" metric), MRR, and the mean
number of searches. Computing all of them side by side shows how much a paper's
choice of metric matters (docs/11-evaluation.md).
"""

import argparse
import json
import sys
from typing import Dict, Iterable, List

from .metrics import exact_match, f1_score, normalize_answer


def cover_em(prediction: str, golds) -> float:
    p = normalize_answer(prediction)
    return float(any(normalize_answer(g) in p for g in golds if normalize_answer(g)))


def retrieval_metrics(retrieved: List[str], gold: List[str], ks=(1, 5, 10)) -> Dict[str, float]:
    gold_set = set(gold)
    out = {}
    for k in ks:
        top = set(retrieved[:k])
        out[f"recall@{k}"] = len(top & gold_set) / len(gold_set)
        out[f"all@{k}"] = float(gold_set <= top)
    rr = 0.0
    for rank, pid in enumerate(retrieved, start=1):
        if pid in gold_set:
            rr = 1.0 / rank
            break
    out["mrr"] = rr
    return out


def evaluate(records: Iterable[dict], ks=(1, 5, 10)) -> Dict[str, float]:
    sums: Dict[str, float] = {}
    counts: Dict[str, int] = {}

    def add(key, val):
        sums[key] = sums.get(key, 0.0) + val
        counts[key] = counts.get(key, 0) + 1

    n = 0
    for r in records:
        n += 1
        golds = r["answers"] if isinstance(r["answers"], list) else [r["answers"]]
        add("em", exact_match(r["prediction"], golds))
        add("f1", f1_score(r["prediction"], golds))
        add("cover_em", cover_em(r["prediction"], golds))
        if r.get("retrieved") is not None and r.get("gold_evidence"):
            for k, v in retrieval_metrics(r["retrieved"], r["gold_evidence"], ks).items():
                add(k, v)
        if "num_searches" in r:
            add("avg_searches", float(r["num_searches"]))
    report = {k: round(100 * sums[k] / counts[k], 2) if k != "avg_searches" else round(sums[k] / counts[k], 3)
              for k in sums}
    report["n"] = n
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path")
    ap.add_argument("--k", type=int, nargs="+", default=[1, 5, 10])
    a = ap.parse_args(argv)
    with open(a.path) as f:
        recs = [json.loads(line) for line in f if line.strip()]
    json.dump(evaluate(recs, a.k), sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
