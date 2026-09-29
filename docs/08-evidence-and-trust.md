# 8. Evidence and trust

A RAG answer is only as trustworthy as (1) the evidence, (2) the model's use of it, and (3) our ability to tell when either failed.

## 8.1 Factuality ≠ faithfulness: FRANQ (Findings ACL 2026)

Note: [papers/2026/franq.md](../papers/2026/franq.md)

|  | Faithful to context | Not faithful to context |
|---|---|---|
| **True** | ideal | correct from parametric memory; *flagged as a hallucination by most detectors* |
| **False** | the retrieved source was wrong | classic hallucination |

FRANQ estimates P(true) by conditioning on faithfulness, using a different uncertainty estimator for each branch. It needs a dataset labelled on *both* axes, which the authors built. The toolkit lineage is [LM-Polygraph](https://github.com/IINemo/lm-polygraph).

**Why it matters for the lecture:** "grounded" metrics (RAGAS faithfulness, ALCE citation support) measure the *columns*. Users care about the *rows*.

## 8.2 Knowledge conflicts
- **Context vs. memory:** ClashEval shows models adopt wrong retrieved facts more often when their prior is weak.
- **Source vs. source:** stale versus fresh documents; an agentic system should prefer recency and authority, but few are trained to.
- **Text vs. image:** CMC-Bench (MAGMaR 2026 workshop, [note](../papers/2026/cmc-bench.md)) finds 0.17–0.46 accuracy drops, 31.7% abstention (Qwen3-VL-4B) and 51.9% fabrication (Gemma-3n-E2B) under conflict. It is an early, single-author signal.

## 8.3 Corpus poisoning and agentic attack surface
- **PoisonedRAG:** about 5 injected passages per target question give about 90% attack success. **BadRAG** ([arXiv:2406.00083](https://arxiv.org/abs/2406.00083)) plants trigger-activated passages.
- **Agentic RAG widens the surface.** The SoK on agentic RAG ([arXiv:2603.07379](https://arxiv.org/abs/2603.07379)) lists hallucination propagation, memory poisoning, retrieval misalignment and cascading tool-execution vulnerabilities.
- **Prompt injection via retrieved content:** a retrieved web page can contain instructions. Treat retrieved text as data, never as instructions.
- **KV-cache side channels:** cache-sharing optimisations (Section 10) can leak which documents other users retrieved; see for example [arXiv:2606.21842](https://arxiv.org/abs/2606.21842).

## 8.4 Practical defences
1. **Provenance:** keep and show source IDs for every claim; evaluate citation precision and recall (ALCE).
2. **Source allow-lists and trust tiers** for what enters the corpus.
3. **Consistency checks:** require agreement across independent sources for high-stakes claims.
4. **Uncertainty-aware abstention:** FRANQ-style scoring to decide when to say "I don't know".
5. **Corpus-grounded triggers:** QuCo-RAG's co-occurrence check doubles as a cheap hallucination flag.
6. **Keep queries auditable.** An argument *against* fully latent retrieval in regulated settings (see [05](05-latent-retrieval.md)).
