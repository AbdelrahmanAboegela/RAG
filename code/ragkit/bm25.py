"""Okapi BM25, the sparse baseline that is still hard to beat.

QuCo-RAG uses BM25 over a Wikipedia dump as its external retriever; HiKEY uses
BM25 as the lexical half of its document router.
"""

import math
from collections import Counter

from .text import tokenize


class BM25:
    def __init__(self, docs, k1: float = 1.5, b: float = 0.75):
        self.docs = list(docs)
        self.k1, self.b = k1, b
        self.tfs = [Counter(tokenize(d, drop_stopwords=True)) for d in self.docs]
        self.lens = [sum(tf.values()) for tf in self.tfs]
        self.avgdl = sum(self.lens) / max(len(self.lens), 1)
        df = Counter()
        for tf in self.tfs:
            df.update(tf.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def score(self, query: str, i: int) -> float:
        tf, dl = self.tfs[i], self.lens[i]
        s = 0.0
        for t in tokenize(query, drop_stopwords=True):
            if t not in tf:
                continue
            f = tf[t]
            s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
        return s

    def search(self, query: str, k: int = 5):
        """Return [(doc_id, score)] sorted by score, zero-score docs dropped."""
        scored = [(i, self.score(query, i)) for i in range(len(self.docs))]
        scored = [x for x in scored if x[1] > 0]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]
