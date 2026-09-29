# Reproducing SPARKLE

**Repo:** [jyfang6/sparkle](https://github.com/jyfang6/sparkle) (linked from the paper) · **Paper:** [ACL 2026 main](https://aclanthology.org/2026.acl-long.1793/) · **Notes:** [papers/2026/sparkle.md](../papers/2026/sparkle.md)

We have not audited the repo's README, so follow it for commands. The paper's setup:

| Component | Paper default |
|---|---|
| Retriever (frozen) | E5 |
| Reader LLM (frozen) | Qwen2.5-7B-Instruct |
| Proxy policy (trained) | Qwen2.5-3B-Instruct |
| Triplet extraction | Llama-3, precomputed and cached (following Fang et al., 2025, KiRAG) |
| RL | PPO with a binary tree-structured rollout and pruning |
| In-domain eval | HotpotQA, 2Wiki, NQ |
| Out-of-domain eval | MuSiQue, Bamboogle, TriviaQA, ASQA |
| Sampling | 1,000 random examples per dataset (all examples for Bamboogle and ASQA) |

**Plug-and-play check:** the paper swaps E5 for BGE and Qwen2.5 for DeepSeek-R1-Distill-Qwen-14B *without retraining* the proxy. Reproducing that transfer is the most informative experiment you can run.
