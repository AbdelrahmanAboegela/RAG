# Reproducing AutoSearch

**Repo:** [bofusun/AutoSearch](https://github.com/bofusun/AutoSearch) · **Paper:** [Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1399/) / [arXiv:2604.17337](https://arxiv.org/abs/2604.17337) · **Notes:** [papers/2026/autosearch.md](../papers/2026/autosearch.md)

The code is built on **verl** and the **Search-R1** codebase, so first follow [search-r1.md](search-r1.md) to get the retriever server and the Wikipedia index running.

## Setup and training (from the repo README)

```bash
git clone https://github.com/bofusun/AutoSearch
conda create -n AutoSearch python=3.8
conda activate AutoSearch
cd AutoSearch
pip install -r requirements.txt

cd experiments
bash train_autosearch.sh
```

At the time of writing, the README does not document data preparation or evaluation separately. Reuse Search-R1's `scripts/data_process/*` for NQ + HotpotQA training data, and its evaluation over NQ, TriviaQA, PopQA, HotpotQA, 2Wiki and Bamboogle.

## What to watch

- **Self-answering.** The rollout template must make the policy emit an intermediate answer after *every* search. The efficiency reward depends on it, because the minimal sufficient depth is defined as the first step whose intermediate answer matches the gold answer.
- **Reward components** (see [`code/ragkit/autosearch_reward.py`](../code/ragkit/autosearch_reward.py) for a readable version): format and outcome base reward, an efficiency term that depends on whether the agent under-searches, stops at the right depth or over-searches, and a quality term (marginal F1 gain per step).
- **Metrics to log**: besides EM, log the *average search depth* and the *over-search ratio*. These are the paper's headline efficiency metrics (for example, Qwen2.5-7B: 48.0 average EM at depth 1.27, against StepSearch's 40.0 at 2.08).
- **Small maximum depth.** The paper studies relatively low search budgets and says so as a limitation. Do not extrapolate its trade-offs to deep-research-style 20–50 call budgets.
