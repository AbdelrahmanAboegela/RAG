"""Score a run with several metrics at once, and see how much the metric choice matters.

    python code/examples/08_evaluate.py
    # or on your own file:
    cd code && python -m ragkit examples/data/toy_run.jsonl --k 1 2 5
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ragkit import evaluate  # noqa: E402

PATH = os.path.join(os.path.dirname(__file__), "data", "toy_run.jsonl")

if __name__ == "__main__":
    with open(PATH) as f:
        recs = [json.loads(line) for line in f if line.strip()]
    for r in recs:
        print(f"- {r['question'][:60]:60s} pred={r['prediction']!r:32s} gold={r['answers']}")
    print(json.dumps(evaluate(recs, ks=(1, 2, 5)), indent=2))
    print("EM, F1 and cover-EM disagree on the same predictions: always state which one you report.")
