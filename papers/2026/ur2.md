# UR²: Unify RAG and Reasoning through Reinforcement Learning

| | |
|---|---|
| **Authors** | Weitao Li, Boran Xiang, Xiaolong Wang, Jingyi Ren, Ante Wang, Zhinan Gou, Weizhi Ma, Yang Liu |
| **Venue / status** | **ACL 2026 main** (Long). First on arXiv in August 2025 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.580/) · [arXiv:2508.06165](https://arxiv.org/abs/2508.06165) · [code](https://github.com/Tsinghua-dhy/UR2) · [models (ModelScope)](https://www.modelscope.cn/collections/UR2-9471aa070f1a46) · [reproduction guide](../../experiments/ur2.md) |
| **Section** | 4, Learned retrieval policies |
| **Verified** | Venue, authors and abstract checked on the ACL Anthology; method details from arXiv v4 (September 2026) |

## TL;DR
UR² trains one policy to reason *and* retrieve across very different domains (open QA, MMLU-Pro, medicine, math). It retrieves only when a problem is hard, and it reads LLM-summarised evidence instead of raw passages. With 3B–8B open models it matches GPT-4o-mini and GPT-4.1-mini on several benchmarks.

## 1. Problem and gap
RL search agents like Search-R1 are trained and tested on open-domain QA, where retrieval is always useful. Put them on math or MMLU-Pro and two failure modes appear:
- **Over-reliance:** the model issues trivial queries to offload reasoning it could do itself.
- **Collapse:** when documents are noisy, the policy learns that retrieval does not pay and falls back to pure chain-of-thought.

## 2. Key idea
Make retrieval **conditional on difficulty** and make evidence **cheap to read**.

## 3. Method
- **Difficulty-aware curriculum.** For each training item, run 20 rollouts and bucket the item by average score: easy (0.8–1.0), medium (0.5–0.8), hard (0.2–0.5). For math, only *hard* items get the retrieval-augmented prompt. Open-domain QA always retrieves.
- **Hybrid knowledge access.** Offline domain corpora (Wikipedia, medical references) are combined with LLM-generated summaries of the retrieved documents, a 14.91× compression in the online setting.
- **Two-stage RL** (REINFORCE++ via OpenRLHF, with retrieved tokens masked):
  - *Stage 1, retrieval activation* (about 10 steps): +1 for valid format, −1 per violation, +3 for issuing one query, +4 for several, −0.5 per fallback error. This teaches the model that searching is an available action.
  - *Stage 2, answer quality*: +2 for a correct answer, +1 for format, −0.5 per fallback error.
- **Training data:** about 3,000 items per task: SimpleZoo-RL (math), the R1-Searcher data (open QA), MedQA, and MMLU-Pro philosophy/history/economics (with synthetic items from Qwen3-32B).
- **Backbones and compute:** Qwen2.5-3B/7B-Instruct and Llama-3.1-8B-Instruct. 8×A100, about 160 GPU-hours, learning rate 2e-6, at most 4 retrieval turns.

## 4. Results
- **Open-domain QA (Qwen2.5-7B):** 58.5 F1 vs 56.1 for Search-R1.
- **MMLU-Pro (7B):** 53.2 vs 50.0 for Open-Reasoner-Zero.
- **Medicine (7B):** 65.9 average vs 60.8 for vanilla RL.
- **Scale:** the largest gains are on the smaller models (up to +29.6%). The 7B model matches GPT-4o-mini and GPT-4.1-mini on several benchmarks.

## 5. Limitations
- **(stated)** Experiments go up to 8B. **(stated)** LLM-summarised corpora do not capture the messiness of raw web content. **(stated)** DeepSeek-R1-distilled models lost tool-use ability after long-CoT training, which suggests brittleness in some model families.
- **(ours)** The summariser is an external LLM, so part of the gain may come from distilling a stronger model's reading. Its cost is not counted in the comparison.

## 6. What changed vs. the previous approach
Search-R1 learns *how* to search on tasks where searching always helps. UR² learns **whether** to search across tasks where it often does not.

## 7. Discussion questions
1. Stage 1 rewards *using* retrieval, regardless of correctness. When does that bootstrapping trick become reward hacking?
2. Difficulty is measured with 20 rollouts per item. Could the model predict its own difficulty at inference time instead? Compare with [QuCo-RAG](quco-rag.md).
