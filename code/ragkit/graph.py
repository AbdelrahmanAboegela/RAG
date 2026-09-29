"""Graph RAG in miniature: a triplet graph + Personalized PageRank (HippoRAG-style).

HippoRAG (Gutiérrez et al., NeurIPS 2024) indexes a corpus as an OpenIE knowledge
graph, seeds Personalized PageRank (PPR) at the entities mentioned in the query,
and ranks passages by the PPR mass of the entities they contain. PPR spreads
probability along edges, so entities two or three hops from the query still get
mass, which is how a single retrieval step can reach multi-hop evidence.
HiGoE (ACL 2026) reuses PPR to organise a proposition-evidence graph.

Triplets are given as (subject, relation, object, passage_id).
"""

from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple


class TripletGraph:
    def __init__(self, triplets: Iterable[Tuple[str, str, str, int]]):
        self.adj: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.passages_of: Dict[str, set] = defaultdict(set)
        for s, r, o, pid in triplets:
            s, o = s.lower(), o.lower()
            self.adj[s][o] += 1.0
            self.adj[o][s] += 1.0  # undirected, as in HippoRAG
            self.passages_of[s].add(pid)
            self.passages_of[o].add(pid)
        self.nodes = sorted(self.adj)

    def personalized_pagerank(self, seeds: Sequence[str], damping: float = 0.5,
                              iters: int = 50, tol: float = 1e-9) -> Dict[str, float]:
        """Power iteration. `damping` = probability of following an edge (HippoRAG uses 0.5)."""
        seeds = [s.lower() for s in seeds if s.lower() in self.adj]
        if not seeds:
            return {}
        reset = {n: (1.0 / len(seeds) if n in seeds else 0.0) for n in self.nodes}
        p = dict(reset)
        for _ in range(iters):
            nxt = {n: (1 - damping) * reset[n] for n in self.nodes}
            for u in self.nodes:
                out = self.adj[u]
                tot = sum(out.values())
                for v, w in out.items():
                    nxt[v] += damping * p[u] * w / tot
            delta = sum(abs(nxt[n] - p[n]) for n in self.nodes)
            p = nxt
            if delta < tol:
                break
        return p

    def rank_passages(self, seeds: Sequence[str], k: int = 5, **kw) -> List[Tuple[int, float]]:
        ppr = self.personalized_pagerank(seeds, **kw)
        score = defaultdict(float)
        for node, mass in ppr.items():
            for pid in self.passages_of[node]:
                score[pid] += mass
        return sorted(score.items(), key=lambda x: -x[1])[:k]
