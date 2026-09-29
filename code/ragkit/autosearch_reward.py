"""AutoSearch-style reward shaping for adaptive search depth.

AutoSearch (Sun et al., Findings of ACL 2026, arXiv:2604.17337) asks the agent to
emit an intermediate answer after every search. The *minimal sufficient search
depth* t_c is the first step whose intermediate answer already matches the gold
answer. Searching less than t_c under-explores; searching more is waste.

The reward has three parts (see docs/04 and papers/2026/autosearch.md):
  1. base reward: format + final-answer correctness (like Search-R1),
  2. efficiency reward: bonus for stopping at or before t_c, penalty per step beyond it,
  3. quality reward: marginal F1 gain of each step over the best previous step.

The constants below follow our reading of the paper and are exposed as arguments.
They are illustrative; check the official repo (github.com/bofusun/AutoSearch)
before using them to reproduce results.
"""

from typing import List, Optional, Sequence

from .metrics import exact_match, f1_score


def minimal_sufficient_depth(intermediate_answers: Sequence[str], gold) -> Optional[int]:
    """1-indexed first step whose intermediate answer is exactly correct, or None."""
    for t, ans in enumerate(intermediate_answers, start=1):
        if exact_match(ans, gold):
            return t
    return None


def autosearch_reward(
    intermediate_answers: List[str],
    final_answer: str,
    gold,
    steps_well_formed: Optional[List[bool]] = None,
    final_well_formed: bool = True,
    eps: float = 1e-6,
    under_search_bonus: float = 0.025,
    effective_scale: float = 0.4,
    effective_offset: float = 0.05,
    over_search_penalty: float = 0.1,
    use_quality: bool = True,
) -> dict:
    n = len(intermediate_answers)
    steps_well_formed = steps_well_formed if steps_well_formed is not None else [True] * n

    # 1) base reward
    base = sum(0.0 if ok else -0.05 for ok in steps_well_formed)
    base += 0.1 if final_well_formed else -0.5
    if exact_match(final_answer, gold):
        base += 1.0

    # 2) efficiency reward relative to the minimal sufficient depth
    t_c = minimal_sufficient_depth(intermediate_answers, gold)
    if t_c is None:
        efficiency = under_search_bonus * n        # never got there: nudge towards searching more
        regime = "under-search"
    elif n <= t_c:
        efficiency = effective_scale / (t_c + eps) - effective_offset
        regime = "effective"
    else:
        efficiency = -over_search_penalty * (n - t_c)
        regime = "over-search"

    # 3) quality reward: sum of marginal F1 gains over the running best
    quality, best = 0.0, 0.0
    if use_quality:
        for ans in intermediate_answers:
            f = f1_score(ans, gold)
            quality += max(0.0, f - best)
            best = max(best, f)

    return {"total": base + efficiency + quality, "base": base, "efficiency": efficiency,
            "quality": quality, "t_c": t_c, "regime": regime, "depth": n}
