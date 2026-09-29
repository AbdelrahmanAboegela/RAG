"""Hybrid sparse + dense retrieval fused with RRF: the production default for 'naive' RAG."""

from .bm25 import BM25
from .dense import DenseIndex
from .fusion import reciprocal_rank_fusion


class HybridRetriever:
    def __init__(self, docs, embedder=None, depth: int = 20):
        self.docs = list(docs)
        self.bm25 = BM25(self.docs)
        self.dense = DenseIndex(self.docs, embedder)
        self.depth = depth

    def search(self, query: str, k: int = 5):
        sparse = self.bm25.search(query, self.depth)
        dense = self.dense.search(query, self.depth)
        return reciprocal_rank_fusion([sparse, dense], top_n=k)

    def retrieve_text(self, query: str, k: int = 3):
        return [self.docs[i] for i, _ in self.search(query, k)]
