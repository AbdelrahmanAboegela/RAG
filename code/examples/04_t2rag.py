"""T²RAG's placeholder-triplet loop on the running example, with rule-based stand-ins for the LLM.

    python code/examples/04_t2rag.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import HybridRetriever, T2RAG, Triplet  # noqa: E402
from corpus import DOCS, QUESTION  # noqa: E402


def decompose(question):
    # What an LLM would emit: two searchable triplets and two fuzzy ones.
    return [
        Triplet("Move (1970)", "directed by", "?d1"),
        Triplet("Méditerranée (1963)", "directed by", "?d2"),
        Triplet("?d1", "nationality", "?c1"),
        Triplet("?d2", "nationality", "?c2"),
    ]


def resolve(triplet, evidence):
    text = " ".join(evidence)
    if triplet.p == "directed by":
        title = triplet.s.split(" (")[0]
        for doc in evidence:
            if doc.startswith(title):
                m = re.search(r"directed by ([A-Z][\w\-]+ [A-Z][\w\-]+)", doc)
                if m:
                    return m.group(1)
    if triplet.p == "nationality":
        for adj in ("American", "French", "British", "German"):
            if re.search(rf"{re.escape(triplet.s)} was an? {adj}", text):
                return adj
    return None


def answer(question, facts):
    nat = [t.o for t in facts if t.p == "nationality"]
    if len(nat) < 2:
        return "unknown"
    return "yes" if nat[0] == nat[1] else "no"


if __name__ == "__main__":
    retriever = HybridRetriever(DOCS)
    pipe = T2RAG(decompose, retriever.retrieve_text, resolve, answer, max_iters=3, k=3)
    ans, state, log = pipe.run(QUESTION)
    for it, t, res in log:
        print(f"iter {it}: {t:45s} -> {res}")
    print("\nresolved facts:", [str(t) for t in state.resolved])
    print("answer:", ans)
