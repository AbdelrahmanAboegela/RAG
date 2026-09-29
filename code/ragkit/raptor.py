"""RAPTOR in miniature: build a tree of recursive cluster summaries, retrieve across levels.

RAPTOR (Sarthi et al., ICLR 2024) embeds chunks, clusters them (GMM + UMAP in the
paper; k-means here), summarises each cluster with an LLM, and repeats on the
summaries until one node is left. "Collapsed tree" retrieval then searches all
nodes, leaves and summaries together, so a query can match a detail (leaf) or a
theme (summary). Compare HiKEY (ACL 2026), which *parses* the author's hierarchy
instead of inducing one by clustering.

`summarize` is injected: pass an LLM call. The default just concatenates first
sentences so the tree is inspectable offline.
"""

import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .dense import HashingEmbedder, cosine


@dataclass
class Node:
    text: str
    level: int
    children: List[int] = field(default_factory=list)
    vec: Optional[list] = None


def _first_sentences(texts: List[str]) -> str:
    return " ".join(t.split(". ")[0].rstrip(".") + "." for t in texts)


def kmeans(vecs, k: int, iters: int = 20, seed: int = 0) -> List[int]:
    rng = random.Random(seed)
    centers = [list(v) for v in rng.sample(vecs, k)]
    assign = [0] * len(vecs)
    for _ in range(iters):
        assign = [max(range(k), key=lambda c: cosine(v, centers[c])) for v in vecs]
        for c in range(k):
            members = [vecs[i] for i, a in enumerate(assign) if a == c]
            if members:
                centers[c] = [sum(col) / len(members) for col in zip(*members)]
    return assign


class RaptorTree:
    def __init__(self, chunks: List[str], branching: int = 3,
                 summarize: Callable[[List[str]], str] = _first_sentences, embedder=None):
        self.embedder = embedder or HashingEmbedder()
        self.nodes: List[Node] = [Node(c, 0, vec=self.embedder.embed(c)) for c in chunks]
        level_ids = list(range(len(self.nodes)))
        level = 0
        while len(level_ids) > 1:
            level += 1
            k = max(1, len(level_ids) // branching)
            assign = kmeans([self.nodes[i].vec for i in level_ids], k)
            next_ids = []
            for c in range(k):
                members = [level_ids[j] for j, a in enumerate(assign) if a == c]
                if not members:
                    continue
                text = summarize([self.nodes[m].text for m in members])
                self.nodes.append(Node(text, level, members, self.embedder.embed(text)))
                next_ids.append(len(self.nodes) - 1)
            if len(next_ids) == len(level_ids):  # clustering made no progress
                break
            level_ids = next_ids
        self.depth = level

    def search(self, query: str, k: int = 3):
        """Collapsed-tree retrieval: rank every node, whatever its level."""
        q = self.embedder.embed(query)
        ranked = sorted(range(len(self.nodes)), key=lambda i: -cosine(q, self.nodes[i].vec))
        return [(i, self.nodes[i].level, self.nodes[i].text) for i in ranked[:k]]
