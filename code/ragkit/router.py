"""Query routing: decide *how much* retrieval a query needs before running anything.

Adaptive-RAG (Jeong et al., NAACL 2024) trains a small classifier that routes each
query to no retrieval, single-step, or multi-step retrieval. UR² (ACL 2026)
applies the same idea inside RL training (retrieve only for hard items), and
Self-Route (Li et al., EMNLP 2024 industry) routes between RAG and long context.

`HeuristicRouter` is a transparent, rule-based stand-in so you can see the
features such routers learn: multi-hop cue words, number of entities, comparison
structure, and whether the entities are rare (a QuCo-RAG-style signal if you pass
a frequency function).
"""

import re
from dataclasses import dataclass
from typing import Callable, Optional

from .quco import naive_entities

_MULTIHOP = re.compile(r"\b(both|same|compare|older|younger|before|after|whose|which .* of|than)\b", re.I)


@dataclass
class Route:
    strategy: str  # "no_retrieval" | "single_step" | "multi_step"
    reason: str


class HeuristicRouter:
    def __init__(self, freq: Optional[Callable[[str], int]] = None, rare_threshold: int = 1000):
        self.freq, self.rare = freq, rare_threshold

    def route(self, question: str) -> Route:
        ents = naive_entities(question)
        if len(ents) >= 2 and _MULTIHOP.search(question):
            return Route("multi_step", f"{len(ents)} entities + comparison/bridge cue")
        if self.freq is not None and ents and all(self.freq(e) >= self.rare for e in ents):
            return Route("no_retrieval", "all entities frequent: likely memorised")
        if not ents:
            return Route("no_retrieval", "no named entity: likely reasoning or chit-chat")
        return Route("single_step", f"entities {ents}")
