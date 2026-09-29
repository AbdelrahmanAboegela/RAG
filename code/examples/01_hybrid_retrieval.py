"""Naive RAG retrieval on the running example: BM25 vs dense vs RRF hybrid.

Shows the core failure that motivates everything after Section 2: a single query
for a 4-hop question cannot retrieve both directors' nationalities.

    python code/examples/01_hybrid_retrieval.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import BM25, DenseIndex, HybridRetriever  # noqa: E402
from corpus import DOCS, QUESTION  # noqa: E402


def show(name, hits):
    print(f"\n== {name}")
    for i, s in hits:
        print(f"  [{s:.3f}] {DOCS[i][:90]}")


if __name__ == "__main__":
    print("Q:", QUESTION)
    show("BM25", BM25(DOCS).search(QUESTION, 3))
    show("Dense (hashing toy embedder)", DenseIndex(DOCS).search(QUESTION, 3))
    show("Hybrid (RRF, k=60)", HybridRetriever(DOCS).search(QUESTION, 3))
    print("\nNote: none of the single-shot top-3 lists contains both nationality passages.")
    print("Multi-hop questions need iterative retrieval -> see 02_agentic_loop.py.")
