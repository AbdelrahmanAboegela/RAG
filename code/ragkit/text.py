"""Tokenisation and chunking.

Chunking is the least glamorous and most consequential choice in a RAG system:
it fixes the unit that the retriever can return. See docs/01-foundations.md.
"""

import re

_TOKEN = re.compile(r"[a-z0-9]+")
_SENT = re.compile(r"(?<=[.!?])\s+")

STOPWORDS = frozenset(
    "a an the of in on at to for from by with and or is are was were be been "
    "who what when where which how did does do this that it its as".split()
)


def tokenize(text: str, drop_stopwords: bool = False):
    toks = _TOKEN.findall(text.lower())
    if drop_stopwords:
        toks = [t for t in toks if t not in STOPWORDS]
    return toks


def chunk_words(text: str, size: int = 100, overlap: int = 20):
    """Fixed-size word windows with overlap (the DPR / Search-R1 '100-word passage' style)."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


def chunk_sentences(text: str, max_words: int = 100):
    """Greedy sentence packing: never split a sentence, close a chunk at max_words."""
    chunks, cur, n = [], [], 0
    for sent in _SENT.split(text.strip()):
        w = len(sent.split())
        if cur and n + w > max_words:
            chunks.append(" ".join(cur))
            cur, n = [], 0
        cur.append(sent)
        n += w
    if cur:
        chunks.append(" ".join(cur))
    return chunks
