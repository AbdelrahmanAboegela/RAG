# SpecCache: Speculative KV Cache Reuse for Efficient RAG Serving

| | |
|---|---|
| **Authors** | Zijian Wen, Tao Zhang, Shuangwu Chen, Shenghao Ye, Yu Guo, Qirui Chen, Jingxian Shuai, Yunpeng Hou, Huasen He, Jianyang … (the Anthology listing is truncated; check the PDF) |
| **Venue / status** | **ACL 2026 main** (Long), pp. 18861–18871 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.859/) · code: not linked |
| **Section** | 10, Efficiency |
| **Verified** | Anthology abstract (September 2026) |

**Problem.** RAG prompts are long, so **prefill** dominates time-to-first-token (TTFT). Documents repeat across queries, so their KV caches could be precomputed and reused. But a document's KV depends on what precedes it (cross-attention to other chunks), so naive reuse degrades quality. CacheBlend-style methods recompute a subset of "important" tokens to repair this.

**Observation.** KV deviations from reuse are **largest in deep layers**, yet reading deep-layer features from the big target model to choose which tokens to recompute would cost almost as much as recomputing everything.

**Method.** Use a small **speculative model's hidden-state norms** to predict which tokens the large model should recompute. This is the speculative-decoding idea applied to cache repair.

**Results.** TTFT falls by **2.17–3.95×** and throughput rises by **2.7–5.2×** vs full recomputation, with negligible quality loss.

**Lineage.** Prompt caching → RAGCache (caching the knowledge tree) → CacheBlend (selective recompute) → **SpecCache** (choosing what to recompute, cheaply).
