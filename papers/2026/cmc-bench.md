# CMC-Bench: "When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation"

| | |
|---|---|
| **Authors** | Jasper Kyle Catapang (single author) |
| **Venue / status** | **Workshop paper**: MAGMaR 2026 (2nd Workshop on Multimodal Augmented Generation via Multimodal Retrieval, co-located with ACL 2026) |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.magmar-main.3/) · code: not linked |
| **Section** | 9, Multimodal (early signal) |
| **Verified** | Anthology abstract (September 2026) |

**Question.** When retrieved text and a retrieved image **contradict each other**, what does a vision-language model do?

**Benchmark.** The Cross-Modal Conflict Benchmark has 3,768 instances built from ChartQA and MMMU splits, with 4 conflict types and several evidence conditions. Four VLMs are evaluated.

**Findings.**
- Accuracy drops by 0.17–0.46 relative to aligned evidence.
- Qwen3-VL-4B **abstains** 31.7% of the time on conflicts.
- Gemma-3n-E2B **fabricates** in 51.9% of conflict cases.

**How to present it.** It is a single-author workshop paper with small models, so present it as an **early signal**, not a settled result. It pairs naturally with Chart-MRAG's text-over-visual bias finding and with text-only knowledge-conflict work (ClashEval, the knowledge-conflicts survey) in [docs/08](../../docs/08-evidence-and-trust.md).
