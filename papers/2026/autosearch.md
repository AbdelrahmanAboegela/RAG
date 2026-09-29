# AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning

| | |
|---|---|
| **Authors** | Jingbo Sun, Wenyue Chong, Songjun Tu, Qichao Zhang, Yaocheng Zhang, Jiajun Chai, Xiaohan Wang, Wei Lin, Guojun Yin, Dongbin Zhao |
| **Venue / status** | **Findings of ACL 2026**, pp. 28059–28079 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.1399/) · [arXiv:2604.17337](https://arxiv.org/abs/2604.17337) · [code](https://github.com/bofusun/AutoSearch) · [reproduction guide](../../experiments/autosearch.md) · [toy reward](../../code/ragkit/autosearch_reward.py) |
| **Section** | 4, Learned retrieval policies (efficiency) |
| **Verified** | Venue and abstract checked on the ACL Anthology; method and numbers from arXiv v1 (September 2026) |

## TL;DR
AutoSearch trains a search agent to stop at the **minimal sufficient search depth**: the first step at which it could already answer correctly. It raises accuracy *and* cuts the number of searches relative to Search-R1 and StepSearch.

## 1. Problem and gap
RL search agents over-search. Each extra retrieval adds latency, tokens and noise. Existing fixes either cap the depth for every question, which hurts hard multi-hop questions, or add a flat per-call penalty, which teaches the agent to under-search.

## 2. Key idea
Make the agent **self-answer** after every search. The first step whose intermediate answer is correct, t_c, is the ideal depth *for this question and this model*. Reward reaching t_c, and penalise going past it.

## 3. Method
- **Self-answering rollout:** after every `<information>` block, the policy emits an intermediate answer.
- **Minimal sufficient depth:** t_c is the earliest step where the intermediate answer exactly matches the gold answer. Empirically this is about 1 for NQ and about 3 for Bamboogle. Stronger models peak later and *degrade* if they keep searching.
- **Reward = base + efficiency + quality:**
  - *Base:* 0 for a valid intermediate step, −0.05 for an invalid one; +0.1 for a valid final answer, −0.5 for an invalid one; +1.0 if the final answer is correct.
  - *Efficiency:* under-search (never correct): +0.025 per step. Effective (depth ≤ t_c): 0.4/(t_c+ε) − 0.05. Over-search (depth > t_c): −0.1 per extra step.
  - *Quality:* the marginal F1 gain of each step over the best previous step.
- **RL:** PPO with GAE and retrieved-token masking. GRPO gives comparable results.
- **Backbones:** Qwen2.5-3B and 7B.

## 4. Results
- **Datasets:** NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, Bamboogle. **Baselines:** Search-R1, StepSearch, HiPRAG.
- **Qwen2.5-3B vs Search-R1-base (EM):** NQ 43.7 vs 36.0; TriviaQA 61.7 vs 51.3; Bamboogle 33.1 vs 16.1.
- **Efficiency (3B):** average depth 1.36 at 44.3 EM, vs 1.52 at 32.9 for Search-R1-base. The over-search ratio is near zero, vs 3–37% for the baselines.
- **Qwen2.5-7B:** 48.0 average EM at depth 1.27, vs 40.0 at depth 2.08 for StepSearch.

## 5. Limitations
- **(stated)** Only low maximum search depths are studied.
- **(ours)** t_c is defined by *exact match* of intermediate answers, so it is only available for short-answer QA with gold labels. It does not transfer directly to long-form answers or deep research.
- **(ours)** Rewarding the first correct intermediate answer may teach the model to commit early on questions where extra verification would be worth it.

## 6. What changed vs. the previous approach
Search-R1 asks "did you get it right?". AutoSearch asks "**did you get it right with no more searching than you needed?**", and it defines "needed" per question from the model's own intermediate answers.

## 7. Discussion questions
1. t_c depends on the current policy, so it moves during training. Is that a feature or a source of instability?
2. How would you define t_c for a long-form answer, where exact match does not exist?
3. Compare with RAG-on-a-Diet, which reduces cost by choosing *smaller models per hop* rather than *fewer hops*. Can the two be combined?
