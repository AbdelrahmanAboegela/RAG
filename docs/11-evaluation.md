# 11. Evaluation, and why numbers don't compare across papers

> **Code:** [`code/ragkit/metrics.py`](../code/ragkit/metrics.py) (EM / F1)

## 11.1 Benchmarks

### Short-answer QA (the RL-search standard)
| Dataset | Type | Notes |
|---|---|---|
| Natural Questions (NQ) | single-hop | Google queries; the standard training set together with HotpotQA |
| TriviaQA | single-hop | trivia |
| PopQA | single-hop, long-tail | entity popularity varies; good for "when to retrieve" |
| HotpotQA | multi-hop (2) | bridge and comparison questions |
| 2WikiMultihopQA | multi-hop (2–4) | the running example's style |
| MuSiQue | multi-hop (2–4) | built to resist shortcuts; hardest of the set |
| Bamboogle | multi-hop | **only 125 questions**, so one question = 0.8 EM |
| SimpleQA | single-hop factuality | adversarially collected against GPT-4 |

### RAG-specific and harder
| Benchmark | What it tests | Link |
|---|---|---|
| **CRAG** (Meta, KDD Cup 2024) | 4.4K QA pairs, 5 domains, dynamic/fast-changing facts, mock web and KG APIs | [arXiv:2406.04744](https://arxiv.org/abs/2406.04744) · 💻 [facebookresearch/CRAG](https://github.com/facebookresearch/CRAG) |
| **FRAMES** (Google) | 824 multi-hop questions that need 2–15 Wikipedia articles; tests retrieval + reasoning + factuality together | [arXiv:2409.12941](https://arxiv.org/abs/2409.12941) · HF `google/frames-benchmark` |
| **MultiHop-RAG** | multi-hop queries over news articles | [arXiv:2401.15391](https://arxiv.org/abs/2401.15391) · 💻 [yixuantt/MultiHop-RAG](https://github.com/yixuantt/MultiHop-RAG) |
| **BRIGHT** | reasoning-intensive *retrieval* | [arXiv:2407.12883](https://arxiv.org/abs/2407.12883) · 💻 [xlang-ai/BRIGHT](https://github.com/xlang-ai/BRIGHT) |
| **BrowseComp** (OpenAI) | hard-to-find web facts; deep-research agents | [arXiv:2504.12516](https://arxiv.org/abs/2504.12516) |
| **ALCE** | citation quality | [arXiv:2305.14627](https://arxiv.org/abs/2305.14627) |
| **KILT** | knowledge-intensive tasks over one Wikipedia snapshot | [arXiv:2009.02252](https://arxiv.org/abs/2009.02252) |
| **RGB** (AAAI 2024) | four RAG abilities: noise robustness, negative rejection, information integration, counterfactual robustness | [arXiv:2309.01431](https://arxiv.org/abs/2309.01431) |
| **BrowseComp-Plus** (ACL 2026) | deep research on a **fixed** ~100K-doc corpus; separates retriever from agent | [note](../papers/2026/browsecomp-plus.md) |
| **CRAG-MM** (KDD 2026) | multimodal, multi-turn, egocentric images | [arXiv:2510.26160](https://arxiv.org/abs/2510.26160) |
| **GraphRAG-Bench** | when graphs help RAG | [arXiv:2506.05690](https://arxiv.org/abs/2506.05690) |
| **LaRA** | RAG vs long context | [arXiv:2502.09977](https://arxiv.org/abs/2502.09977) |
| Domain: MIRAGE (medicine), Legal RAG Bench, FinanceBench | domain RAG | [16](16-domain-and-enterprise-rag.md) |
| Deep research: ResearchRubrics, FINDER, MMDR-Bench, MiroEval, DRB | report-level evaluation | [13](13-deep-research.md) |
| LoCoMo / LongMemEval | long-term conversational memory | §6 |
| M3DocVQA, Chart-MRAG | multimodal document RAG | §9 |

### Metrics
- **EM / F1** (SQuAD normalisation): brittle to phrasing ("USA" vs "United States").
- **Cover-EM / Acc:** the gold answer appears anywhere in the output. More lenient.
- **LLM-as-judge accuracy:** robust to phrasing; judge bias and cost.
- **Retrieval:** Recall@k, MRR, nDCG; "All" (every gold document retrieved; HiKEY).
- **Grounding:** faithfulness and context precision/recall ([RAGAS](https://github.com/explodinggradients/ragas), [ARES](https://github.com/stanford-futuredata/ARES)); citation precision/recall (ALCE).
- **Efficiency:** number of searches, over-search ratio (AutoSearch), TTFT, latency, cost.

## 11.2 Why you can't compare numbers across papers

Put this slide in every RAG talk. On the "same" HotpotQA, papers differ in:

1. **Backbone:** Qwen2.5-3B vs 7B vs Qwen3-8B vs Llama-3.1-8B; **Base vs Instruct**.
2. **Retriever and corpus:** E5 vs BGE vs Qwen3-Embedding; Wikipedia 2018 vs 2023 vs Google Search. State-Aware RAG gets **+22.2%** from the corpus alone.
3. **Top-k and maximum turns.**
4. **Split and sample:** full dev set vs a random 1,000; Bamboogle's 125.
5. **Metric:** EM vs F1 vs cover-EM vs LLM-judge accuracy. The State-Aware RAG, SPARKLE and QuCo-RAG papers report different metrics on the same datasets.
6. **Baselines re-run by the authors,** often with weaker settings than the original papers.

**Rule:** compare *within* a paper's table, never across papers. When you must compare across papers, rerun both methods under one protocol (FlashRAG helps).

## 11.3 Saturation risk
Most RL-search papers train on NQ + HotpotQA and test on the same seven sets, which reward short entity answers. That favours methods tuned to that format, and says little about long-form, enterprise, multilingual or multimodal RAG.
