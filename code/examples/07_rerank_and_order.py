"""Retrieve wide, rerank, diversify, then order for the reader.

    python code/examples/07_rerank_and_order.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import HybridRetriever, HashingEmbedder, ProximityReranker, lost_in_the_middle_order, mmr  # noqa: E402
from corpus import DOCS  # noqa: E402

QUERY = "Jean-Daniel Pollet nationality French filmmaker"

if __name__ == "__main__":
    cands = [i for i, _ in HybridRetriever(DOCS).search(QUERY, 8)]
    print("hybrid candidates   :", cands)
    rr = ProximityReranker().rerank(QUERY, [DOCS[i] for i in cands])
    reranked = [cands[j] for j, _ in rr]
    print("after rerank        :", reranked)
    emb = HashingEmbedder()
    picked = mmr(emb.embed(QUERY), [emb.embed(DOCS[i]) for i in reranked], k=4, lam=0.7)
    diverse = [reranked[j] for j in picked]
    print("after MMR (k=4)     :", diverse)
    print("lost-in-middle order:", lost_in_the_middle_order(diverse), "(best first and last)")
