"""Answer caching for RAG, with the safety gates that make reuse correct.

Naive semantic caches return a stored answer whenever a new query is *similar*
to an old one. That is unsafe: similar questions can have different answers, and
the corpus changes. GroundedCache (arXiv:2605.27494) admits a cached answer only
if cheap gates all pass; FinCacheServe (arXiv:2607.26076) keys answers on
document versions and evidence fingerprints. This module implements four gates:

  1. query similarity      >= sim_threshold
  2. evidence overlap      (Jaccard of retrieved passage ids) >= overlap_threshold
  3. source-version check  every passage the answer used is still at the same version
  4. lexical support       the cached answer's tokens appear in the fresh evidence
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

from .dense import HashingEmbedder, cosine
from .text import tokenize


@dataclass
class CacheEntry:
    query: str
    query_vec: list
    answer: str
    evidence_ids: frozenset
    versions: Dict[str, int]


@dataclass
class CacheDecision:
    hit: bool
    answer: Optional[str] = None
    failed_gate: Optional[str] = None
    detail: dict = field(default_factory=dict)


class GroundedAnswerCache:
    def __init__(self, embedder=None, sim_threshold: float = 0.9, overlap_threshold: float = 0.5,
                 support_threshold: float = 1.0):
        self.embedder = embedder or HashingEmbedder()
        self.sim_t, self.ovl_t, self.sup_t = sim_threshold, overlap_threshold, support_threshold
        self.entries: List[CacheEntry] = []

    def put(self, query: str, answer: str, evidence_ids: Sequence[str], versions: Dict[str, int]):
        self.entries.append(CacheEntry(query, self.embedder.embed(query), answer,
                                       frozenset(evidence_ids), dict(versions)))

    def get(self, query: str, fresh_evidence: Dict[str, str], current_versions: Dict[str, int]) -> CacheDecision:
        """`fresh_evidence`: {passage_id: text} retrieved for *this* query right now."""
        if not self.entries:
            return CacheDecision(False, failed_gate="empty")
        qv = self.embedder.embed(query)
        e = max(self.entries, key=lambda x: cosine(qv, x.query_vec))
        sim = cosine(qv, e.query_vec)
        if sim < self.sim_t:
            return CacheDecision(False, failed_gate="similarity", detail={"sim": sim})
        fresh_ids = set(fresh_evidence)
        overlap = len(e.evidence_ids & fresh_ids) / max(len(e.evidence_ids | fresh_ids), 1)
        if overlap < self.ovl_t:
            return CacheDecision(False, failed_gate="evidence_overlap", detail={"overlap": overlap})
        stale = [p for p, v in e.versions.items() if current_versions.get(p) != v]
        if stale:
            return CacheDecision(False, failed_gate="source_version", detail={"stale": stale})
        ans_toks = set(tokenize(e.answer, drop_stopwords=True))
        ev_toks = set(tokenize(" ".join(fresh_evidence.values())))
        support = len(ans_toks & ev_toks) / max(len(ans_toks), 1)
        if support < self.sup_t:
            return CacheDecision(False, failed_gate="lexical_support", detail={"support": support})
        return CacheDecision(True, e.answer, detail={"sim": sim, "overlap": overlap, "support": support})
