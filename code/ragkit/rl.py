"""The RL arithmetic behind Search-R1-style training, on plain Python lists.

* `group_relative_advantages`: GRPO (DeepSeekMath, arXiv:2402.03300). Sample G
  rollouts per question, advantage_i = (r_i - mean(r)) / (std(r) + eps). No critic.
* `masked_policy_loss`: PPO-clip surrogate averaged over *model-generated* tokens
  only. Tokens inside <information> (retrieved text) have mask 0, exactly as in
  Search-R1: the policy is not credited or blamed for text the retriever wrote.
* `token_mask_from_steps`: build that mask from an `agentic.Trajectory`.

Real training computes these on GPU tensors inside verl/OpenRLHF/TRL; the maths is
the same.
"""

import math
from typing import List, Sequence


def group_relative_advantages(rewards: Sequence[float], eps: float = 1e-6, normalize_std: bool = True):
    n = len(rewards)
    mean = sum(rewards) / n
    if not normalize_std:
        return [r - mean for r in rewards]
    std = math.sqrt(sum((r - mean) ** 2 for r in rewards) / n)
    return [(r - mean) / (std + eps) for r in rewards]


def masked_policy_loss(logp_new: Sequence[float], logp_old: Sequence[float], advantage: float,
                       mask: Sequence[int], clip_eps: float = 0.2) -> float:
    """-(1/|mask|) * sum_t mask_t * min(ratio_t * A, clip(ratio_t, 1-eps, 1+eps) * A)."""
    total, count = 0.0, 0
    for ln, lo, m in zip(logp_new, logp_old, mask):
        if not m:
            continue
        ratio = math.exp(ln - lo)
        clipped = max(min(ratio, 1 + clip_eps), 1 - clip_eps)
        total += min(ratio * advantage, clipped * advantage)
        count += 1
    return -total / count if count else 0.0


def token_mask_from_steps(steps, tokenize=str.split) -> List[int]:
    """1 for tokens the policy generated, 0 for tokens the environment inserted."""
    mask = []
    for s in steps:
        mask.extend([1 if s.is_model_generated else 0] * len(tokenize(s.text)))
    return mask
