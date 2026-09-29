"""QuCo-RAG: decide *when* to retrieve from pre-training corpus statistics.

QuCo-RAG (Min et al., Findings of ACL 2026, arXiv:2512.19134) replaces
model-internal uncertainty (entropy, logit confidence) with two corpus checks:

  Stage 1, before generation: if any entity in the question is rare in the
  pre-training corpus (frequency < tau_entity, 10^3 in the paper), the model has
  probably not memorised it -> retrieve with the original question.

  Stage 2, during generation: for each generated claim (head, relation, tail),
  check whether head and tail ever co-occur within a window (1,000 tokens in the
  paper). Zero co-occurrence is strong evidence of a hallucinated link ->
  retrieve with "head relation" and regenerate.

The paper queries OLMo-2's ~4T-token corpus through Infini-gram. Here the
corpus is abstracted behind `CorpusStats`, with an in-memory implementation for
tests and an optional Infini-gram HTTP client.
"""

import json
import re
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Tuple

from .text import tokenize


class CorpusStats:
    def count(self, phrase: str) -> int:
        raise NotImplementedError

    def cooccur(self, a: str, b: str, window: int = 1000) -> int:
        raise NotImplementedError


class InMemoryCorpusStats(CorpusStats):
    """Exact phrase counts and windowed co-occurrence over a small list of documents."""

    def __init__(self, docs: Sequence[str]):
        self.docs = [tokenize(d) for d in docs]

    @staticmethod
    def _positions(toks, phrase_toks):
        n = len(phrase_toks)
        return [i for i in range(len(toks) - n + 1) if toks[i:i + n] == phrase_toks]

    def count(self, phrase: str) -> int:
        p = tokenize(phrase)
        return sum(len(self._positions(d, p)) for d in self.docs) if p else 0

    def cooccur(self, a: str, b: str, window: int = 1000) -> int:
        pa, pb = tokenize(a), tokenize(b)
        total = 0
        for d in self.docs:
            xs, ys = self._positions(d, pa), self._positions(d, pb)
            total += sum(1 for x in xs for y in ys if abs(x - y) <= window)
        return total


class InfiniGramStats(CorpusStats):
    """Thin client for https://api.infini-gram.io (network required; not used in tests).

    Index names are listed at https://infini-gram.readthedocs.io/en/latest/api.html,
    e.g. 'v4_olmo-2-1124-13b-instruct_llama'. Co-occurrence uses a CNF AND query,
    whose clauses may be at most `max_diff_tokens` (<= 1000) apart.
    """

    URL = "https://api.infini-gram.io/"

    def __init__(self, index: str, timeout: float = 10.0):
        self.index, self.timeout = index, timeout

    def _count(self, query: str, **extra) -> int:
        payload = {"index": self.index, "query_type": "count", "query": query, **extra}
        req = urllib.request.Request(self.URL, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return int(json.load(r).get("count", 0))

    def count(self, phrase: str) -> int:
        return self._count(phrase)

    def cooccur(self, a: str, b: str, window: int = 1000) -> int:
        return self._count(f"{a} AND {b}", max_diff_tokens=min(window, 1000))


_CAPSPAN = re.compile(r"\b(?:[A-Z][\w'\-éèà]*(?:\s+(?:of|the|de|\(\d{4}\)|[A-Z][\w'\-éèà]*))*)")


def naive_entities(text: str) -> List[str]:
    """Capitalised-span heuristic. The paper uses a fine-tuned Qwen2.5-0.5B extractor instead."""
    stop = {"The", "A", "An", "Are", "Is", "Was", "Were", "Who", "What", "When", "Where", "Which",
            "Did", "Do", "Does", "How", "And", "In", "Of"}
    out = []
    for span in _CAPSPAN.findall(text):
        words = span.split()
        while words and (words[0] in stop or words[0].lower() in {"of", "the", "de"}):
            words = words[1:]
        while words and words[-1].islower():
            words = words[:-1]
        if words and words[0][0].isupper():
            out.append(" ".join(words))
    return out


@dataclass
class QuCoDecision:
    retrieve: bool
    reason: str
    query: Optional[str] = None
    evidence: dict = field(default_factory=dict)


class QuCoTrigger:
    def __init__(self, stats: CorpusStats, tau_entity: int = 1000, tau_cooc: int = 1, window: int = 1000,
                 entity_extractor: Callable[[str], List[str]] = naive_entities):
        self.stats = stats
        self.tau_entity, self.tau_cooc, self.window = tau_entity, tau_cooc, window
        self.extract = entity_extractor

    def before_generation(self, question: str) -> QuCoDecision:
        freqs = {e: self.stats.count(e) for e in self.extract(question)}
        rare = [e for e, f in freqs.items() if f < self.tau_entity]
        if rare:
            return QuCoDecision(True, f"rare entities: {rare}", question, freqs)
        return QuCoDecision(False, "all entities frequent", None, freqs)

    def during_generation(self, claims: Sequence[Tuple[str, str, str]]) -> QuCoDecision:
        """`claims` are (head, relation, tail) triplets extracted from the sentence just generated."""
        for h, r, t in claims:
            c = self.stats.cooccur(h, t, self.window)
            if c < self.tau_cooc:
                return QuCoDecision(True, f"'{h}' and '{t}' never co-occur", f"{h} {r}", {"cooc": c})
        return QuCoDecision(False, "all claims supported by co-occurrence")
