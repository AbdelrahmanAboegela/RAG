"""SQuAD-style answer normalisation, Exact Match and token F1.

Almost every paper in this repo (Search-R1, AutoSearch, UR2, LatentRAG, QuCo-RAG,
T2RAG, SPARKLE) reports EM and/or F1 computed this way on NQ, HotpotQA, 2Wiki,
MuSiQue, Bamboogle, etc. Small differences in normalisation are one reason why
numbers from different papers are not directly comparable.
"""

import re
import string
from collections import Counter

_ARTICLES = re.compile(r"\b(a|an|the)\b")
_PUNCT = set(string.punctuation)


def normalize_answer(s: str) -> str:
    s = s.lower()
    s = "".join(ch for ch in s if ch not in _PUNCT)
    s = _ARTICLES.sub(" ", s)
    return " ".join(s.split())


def exact_match(prediction: str, gold) -> float:
    """1.0 if the normalised prediction equals any normalised gold answer."""
    golds = [gold] if isinstance(gold, str) else list(gold)
    p = normalize_answer(prediction)
    return float(any(p == normalize_answer(g) for g in golds))


def f1_score(prediction: str, gold) -> float:
    """Max token-level F1 against any gold answer."""
    golds = [gold] if isinstance(gold, str) else list(gold)
    best = 0.0
    p_toks = normalize_answer(prediction).split()
    for g in golds:
        g_toks = normalize_answer(g).split()
        common = Counter(p_toks) & Counter(g_toks)
        same = sum(common.values())
        if not p_toks or not g_toks:
            best = max(best, float(p_toks == g_toks))
            continue
        if same == 0:
            continue
        precision = same / len(p_toks)
        recall = same / len(g_toks)
        best = max(best, 2 * precision * recall / (precision + recall))
    return best
