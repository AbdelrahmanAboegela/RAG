# 10. Efficiency

RAG cost has four parts: **retrieval latency**, **prefill** of long contexts, **decoding** of reasoning and queries, and the **number of steps**. 2026 work attacks each.

| Cost | Technique | Paper |
|---|---|---|
| Number of steps | learn the minimal sufficient search depth | **AutoSearch** ([note](../papers/2026/autosearch.md)) |
| Cost per step | pick the model size per hop | **RAG-on-a-Diet** ([note](../papers/2026/rag-on-a-diet.md)) |
| Decoding thoughts and queries | latent tokens in one forward pass | **LatentRAG** ([note](../papers/2026/latentrag.md)) |
| Prefill of retrieved docs | reuse precomputed KV caches, repair selectively | RAGCache → CacheBlend → **SpecCache** ([note](../papers/2026/speccache.md)) |
| Tokens between iterations | pass triplets, not chain-of-thought | **T²RAG** ([note](../papers/2026/t2rag.md)) |
| Tokens of evidence | budgeted, structure-aware packing | **HiKEY** ([note](../papers/2026/hikey.md)) |
| Retrieval calls when unnecessary | trigger only on rare or unsupported entities | **QuCo-RAG** ([note](../papers/2026/quco-rag.md)) |

## 10.1 KV-cache reuse for RAG

1. **Prefix caching** (vLLM, SGLang): reuse KV for identical *prefixes*. It helps system prompts but not retrieved documents in varying order.
2. **RAGCache** ([arXiv:2404.12457](https://arxiv.org/abs/2404.12457)): caches document KV in a *knowledge tree* keyed by document order, across GPU and host memory.
3. **CacheBlend** ([arXiv:2405.16444](https://arxiv.org/abs/2405.16444), part of [LMCache](https://github.com/LMCache/LMCache)): reuse each document's KV even when it is not a prefix, and **recompute a small subset of tokens** to restore cross-attention between documents.
4. **SpecCache** (ACL 2026 main): *which* tokens to recompute? KV deviations are biggest in deep layers, but probing the big model is expensive, so a **small speculative model's hidden-state norms** choose. TTFT falls 2.17–3.95× and throughput rises 2.7–5.2× vs full recompute, with negligible quality loss.

5. **CacheClip** ([arXiv:2510.10129](https://arxiv.org/abs/2510.10129)): a small auxiliary LLM's last-layer attention picks the tokens to recompute (the same idea as SpecCache); shared prefixes remove repeated attention sinks. Up to 3.33× faster prefill at 20% recompute.
6. **PCR** ([arXiv:2603.23049](https://arxiv.org/abs/2603.23049)): a *systems* view. Look-ahead LRU using the scheduler queue, layer-wise overlap of KV loading with compute, and SSD→DRAM prefetch. Up to 2.47× faster TTFT.

**Security note:** shared non-prefix KV caches leak across users. **SpliceLeak** ([arXiv:2606.21842](https://arxiv.org/abs/2606.21842)) extracts other users' prompts through TTFT timing on vLLM + LMCache. See [15](15-security.md).

## 10.1b Answer caching (skip the LLM entirely), safely

Semantic answer caches are fragile: similar questions can have different answers, and documents change.
- **GroundedCache** ([arXiv:2605.27494](https://arxiv.org/abs/2605.27494)) serves a cached answer only if four gates pass: query similarity, evidence overlap, source version, and lexical support in *fresh* evidence. The unsafe-served rate drops from 15–35% to 0% on HotpotQA regimes, at 1.04–1.07× the no-cache latency. Lexical support is the load-bearing gate.
- **FinCacheServe** ([arXiv:2607.26076](https://arxiv.org/abs/2607.26076)) keys answers by document version, evidence and tool fingerprints, model and decoding config. It skips about 53% of LLM calls on SEC-filing workloads with no stale outputs observed.
- Toy implementation with all four gates: [`code/ragkit/cache.py`](../code/ragkit/cache.py).

## 10.2 A latency budget for the running example (illustrative)

| System | Steps | Decoded tokens (thoughts + queries) | Relative latency |
|---|---|---|---|
| Naive RAG | 1 retrieval | 0 | 1× (and wrong) |
| Search-R1 | 4–5 retrievals | hundreds | about 16–22× (LatentRAG's measurement) |
| AutoSearch | 4 retrievals | hundreds | less, by avoiding the 5th |
| LatentRAG | 4 retrievals | 0 (latent) | about 2× |

## 10.3 Measuring efficiency honestly
Report **TTFT**, **end-to-end latency**, **number of retrieval calls**, **generated tokens**, and **money** if models of different sizes are mixed, all on the same hardware. A single "speed-up" number without its baseline and hardware is not comparable.
