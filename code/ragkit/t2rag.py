"""T²RAG: triplet-driven iterative retrieval, without building a graph.

T²RAG (Gong et al., Findings of ACL 2026, arXiv:2508.02435):
  * Index: extract (subject, predicate, object) triplets from chunks, verbalise
    them as short sentences, embed them; keep a pointer to the source chunk.
  * Query: an LLM decomposes the question into triplets with '?' placeholders.
      resolved   = 0 placeholders  (a known fact)
      searchable = 1 placeholder   (retrieve now)
      fuzzy      = 2+ placeholders (wait until another triplet fills one slot)
  * Loop (N=3 in the paper): retrieve for searchable triplets, let the LLM fill
    placeholders, propagate newly bound entities into fuzzy triplets, repeat.
  * Answer from the resolved triplets (+ source chunks).

Only compact triplets travel between iterations, which is where the reported
~45% retrieval-stage token saving over IRCoT comes from.

LLM calls are injected as plain functions so the loop is testable offline.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

PH = "?"


@dataclass(frozen=True)
class Triplet:
    s: str  # an entity, or a placeholder variable such as '?x'
    p: str
    o: str

    @property
    def placeholders(self) -> int:
        return int(self.s.startswith(PH)) + int(self.o.startswith(PH))

    def as_query(self) -> str:
        return " ".join(x for x in (self.s, self.p, self.o) if not x.startswith(PH))

    def bind(self, var: str, value: str) -> "Triplet":
        return Triplet(value if self.s == var else self.s, self.p, value if self.o == var else self.o)

    def __str__(self):
        return f"({self.s}, {self.p}, {self.o})"


def classify(t: Triplet) -> str:
    return {0: "resolved", 1: "searchable"}.get(t.placeholders, "fuzzy")


@dataclass
class TripletState:
    resolved: List[Triplet] = field(default_factory=list)
    searchable: List[Triplet] = field(default_factory=list)
    fuzzy: List[Triplet] = field(default_factory=list)
    bindings: Dict[str, str] = field(default_factory=dict)

    def add(self, t: Triplet):
        getattr(self, classify(t)).append(t)

    def apply_bindings(self):
        """Substitute known variable values into fuzzy triplets and re-bucket them."""
        pending, self.fuzzy = self.fuzzy, []
        for t in pending:
            for var, val in self.bindings.items():
                t = t.bind(var, val)
            self.add(t)


class T2RAG:
    def __init__(self,
                 decompose: Callable[[str], List[Triplet]],
                 retrieve: Callable[[str, int], List[str]],
                 resolve: Callable[[Triplet, List[str]], Optional[str]],
                 answer: Callable[[str, List[Triplet]], str],
                 max_iters: int = 3, k: int = 3):
        self.decompose, self.retrieve, self.resolve, self.answer = decompose, retrieve, resolve, answer
        self.max_iters, self.k = max_iters, k

    def run(self, question: str):
        state = TripletState()
        for t in self.decompose(question):
            state.add(t)
        log = []
        for it in range(1, self.max_iters + 1):
            if not state.searchable:
                break
            batch, state.searchable = state.searchable, []
            for t in batch:
                evidence = self.retrieve(t.as_query(), self.k)
                value = self.resolve(t, evidence)
                var = t.s if t.s.startswith(PH) else t.o
                if value is None:
                    log.append((it, str(t), "unresolved"))
                    continue
                state.bindings[var] = value
                state.resolved.append(t.bind(var, value))
                log.append((it, str(t), f"{var} = {value}"))
            state.apply_bindings()
        return self.answer(question, state.resolved), state, log
