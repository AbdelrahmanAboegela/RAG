"""Reciprocal Rank Fusion (Cormack, Clarke & Buettcher, SIGIR 2009).

RRF combines ranked lists without calibrating their scores:
    score(d) = sum over lists L of 1 / (k + rank_L(d))
k=60 is the value from the original paper and the default in most engines.
"""

from collections import defaultdict


def reciprocal_rank_fusion(ranked_lists, k: int = 60, top_n: int = None):
    """ranked_lists: iterable of [(doc_id, score), ...] or [doc_id, ...], best first."""
    fused = defaultdict(float)
    for lst in ranked_lists:
        for rank, item in enumerate(lst, start=1):
            doc_id = item[0] if isinstance(item, tuple) else item
            fused[doc_id] += 1.0 / (k + rank)
    out = sorted(fused.items(), key=lambda x: -x[1])
    return out[:top_n] if top_n else out
