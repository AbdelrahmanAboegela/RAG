# Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning

| | |
|---|---|
| **Authors** | Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Ö. Arık, Dong Wang, Hamed Zamani, Jiawei Han |
| **Venue / status** | COLM 2025; arXiv March 2025 |
| **Links** | [arXiv:2503.09516](https://arxiv.org/abs/2503.09516) · [code](https://github.com/PeterGriffinJin/Search-R1) · [reproduction guide](../../experiments/search-r1.md) |
| **Section** | 4, Learned retrieval policies (the bridge from 2025) |
| **Verified** | Repo and README checked September 2026 |

## TL;DR
Search-R1 applies DeepSeek-R1-style outcome-reward RL to an LLM that can call a search engine in the middle of its reasoning. The model *learns* when to search, what to search for, and when to stop, using only a final-answer exact-match reward.

## 1. Problem and gap
Before Search-R1, multi-step RAG was either **prompted** (IRCoT, Self-Ask, ReAct, Search-o1), where the retrieval behaviour depends on a frozen model following instructions, or **supervised** (Self-RAG, Toolformer), which needs labelled retrieval trajectories that are expensive to create and cap the policy at the quality of the labels. DeepSeek-R1 (January 2025) showed that outcome-only RL can elicit long reasoning. The open question was whether the same recipe works when the environment includes a non-differentiable search engine.

## 2. Key idea
Treat the search engine as part of the environment. Roll out trajectories that interleave `<think>`, `<search>`, `<information>` and `<answer>`, and reward only whether the final answer is right. **Mask retrieved tokens out of the loss**, so the policy is trained only on the tokens it generated.

```
question ─► LLM ─► <search>q1</search> ─► retriever ─► <information>…</information>
                ─► <search>q2</search> ─► retriever ─► <information>…</information>
                ─► <answer>a</answer> ─► reward = EM(a, gold)
```

## 3. Method
- **Rollout:** generation stops at `</search>` or `</answer>`. On a search, the top-k passages (E5 over the 2018 Wikipedia dump) are appended, and generation resumes. There is a maximum number of turns.
- **RL:** PPO or GRPO (implemented in verl), with a KL penalty to the reference model.
- **Loss masking:** tokens inside `<information>` are excluded from the policy-gradient and KL terms. The ablation shows this matters for stability.
- **Reward:** exact match of the extracted answer. There is no format reward and no process reward.
- **Training data:** NQ + HotpotQA training sets merged.

## 4. Results
- **Backbones:** Qwen2.5-3B and 7B (Base and Instruct), and Llama-3.2-3B in early versions.
- **Evaluation:** seven QA sets: NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue, Bamboogle.
- **Result:** large relative gains over RAG, IRCoT, Search-o1, SFT and R1-without-search baselines. The exact percentages differ across arXiv versions, so quote the version you cite.
- **Findings that shaped later work:** GRPO converges faster, but PPO is more stable. Base models learn the format too. Response length first drops and then rises during training.

## 5. Limitations
- An outcome-only reward gives no credit for good *intermediate* queries. This motivates StepSearch, AutoSearch's quality reward, and process rewards.
- There is no cost term, so the agent over-searches easily. AutoSearch and RAG-on-a-Diet address this.
- The retriever is static Wikipedia. [The Retrieval Bottleneck](../2026/retrieval-bottleneck.md) later shows the retriever sets the performance ceiling.
- It is evaluated only on short-answer QA with EM, and those benchmarks are saturating.

## 6. What changed vs. the previous approach
Retrieval behaviour went from **engineered** (prompts, thresholds, supervised labels) to **learned from the outcome**. That is the thesis of this whole repo.

## 7. Discussion questions
1. Why does masking retrieved tokens stabilise training? What would the gradient push the model to do without it?
2. Search-R1 uses EM as its reward. What behaviours might a policy learn that raise EM without raising real answer quality?
3. [LatentRAG](../2026/latentrag.md) distils Search-R1 trajectories into latent tokens. What does it inherit, good and bad?
