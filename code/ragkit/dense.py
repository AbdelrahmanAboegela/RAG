"""A toy dense retriever.

Real systems use a trained bi-encoder (E5, BGE, Qwen3-Embedding, NV-Embed-v2)
plus an ANN index (FAISS/HNSW). To stay dependency-free we use feature hashing
of word unigrams + character trigrams. It captures fuzzy lexical overlap, which
is enough to demonstrate hybrid retrieval and fusion. Swap `HashingEmbedder` for
any object with an `embed(text) -> list[float]` method to use a real model.
"""

import hashlib
import math

from .text import tokenize


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class HashingEmbedder:
    def __init__(self, dim: int = 512):
        self.dim = dim

    def _h(self, feat: str) -> int:
        return int(hashlib.md5(feat.encode()).hexdigest(), 16)

    def embed(self, text: str):
        v = [0.0] * self.dim
        for tok in tokenize(text, drop_stopwords=True):
            feats = [f"w:{tok}"] + [f"c:{tok[i:i + 3]}" for i in range(max(len(tok) - 2, 1))]
            for f in feats:
                h = self._h(f)
                v[h % self.dim] += 1.0 if (h >> 20) & 1 else -1.0
        return v


class DenseIndex:
    def __init__(self, docs, embedder=None):
        self.docs = list(docs)
        self.embedder = embedder or HashingEmbedder()
        self.vecs = [self.embedder.embed(d) for d in self.docs]

    def search(self, query: str, k: int = 5):
        q = self.embedder.embed(query)
        scored = sorted(((i, cosine(q, v)) for i, v in enumerate(self.vecs)), key=lambda x: -x[1])
        return scored[:k]
