"""Post-retrieval processing: reranking, diversification, and position-aware ordering.

* `ProximityReranker` is a toy stand-in for a cross-encoder: it scores query and
  document *jointly* (term coverage + term proximity), which a bi-encoder cannot do.
  Real systems use BGE-reranker, monoT5, or LLM rerankers (RankGPT, Rank1).
* `mmr` is Maximal Marginal Relevance (Carbonell & Goldstein, SIGIR 1998): trade
  relevance against redundancy so top-k does not contain five copies of one fact.
* `lost_in_the_middle_order` places the strongest passages at the start and end of
  the context, because LLMs use those positions best (Liu et al., TACL 2024).
"""

from typing import Callable, List, Sequence, Tuple

from .dense import cosine
from .text import tokenize


class ProximityReranker:
    def __init__(self, window: int = 8, coverage_weight: float = 1.0, proximity_weight: float = 0.5):
        self.window = window
        self.cw, self.pw = coverage_weight, proximity_weight

    def score(self, query: str, doc: str) -> float:
        q = set(tokenize(query, drop_stopwords=True))
        d = tokenize(doc, drop_stopwords=True)
        if not q or not d:
            return 0.0
        coverage = len(q & set(d)) / len(q)
        # best number of distinct query terms inside any window of `window` tokens
        best = 0
        for i in range(len(d)):
            best = max(best, len(q & set(d[i:i + self.window])))
        proximity = best / len(q)
        return self.cw * coverage + self.pw * proximity

    def rerank(self, query: str, docs: Sequence[str], k: int = None) -> List[Tuple[int, float]]:
        scored = sorted(((i, self.score(query, d)) for i, d in enumerate(docs)), key=lambda x: -x[1])
        return scored[:k] if k else scored


def mmr(query_vec, doc_vecs, k: int = 5, lam: float = 0.7, sim: Callable = cosine) -> List[int]:
    """Greedy MMR: argmax  lam*sim(q,d) - (1-lam)*max_{s in selected} sim(d,s)."""
    selected, candidates = [], list(range(len(doc_vecs)))
    while candidates and len(selected) < k:
        def gain(i):
            red = max((sim(doc_vecs[i], doc_vecs[j]) for j in selected), default=0.0)
            return lam * sim(query_vec, doc_vecs[i]) - (1 - lam) * red
        best = max(candidates, key=gain)
        selected.append(best)
        candidates.remove(best)
    return selected


def lost_in_the_middle_order(items_best_first: Sequence) -> list:
    """[1,2,3,4,5] (best first) -> [1,3,5,4,2]: best at the front, second-best at the end."""
    front, back = [], []
    for i, x in enumerate(items_best_first):
        (front if i % 2 == 0 else back).append(x)
    return front + back[::-1]
