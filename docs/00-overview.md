# 0. Overview: from a pipeline you engineer to a policy the model learns

## The thesis

In 2020, RAG was a **pipeline**: retrieve k passages with a fixed retriever, paste them in front of the question, generate. Every decision (when to retrieve, what query to send, how many passages, how to read them) was a design choice made by an engineer.

By 2026, those decisions are increasingly **learned**:

| Decision | 2020 pipeline | 2023–24 "advanced RAG" | 2025–26 learned policy |
|---|---|---|---|
| **When** to retrieve | always, once | uncertainty thresholds (FLARE, DRAGIN); reflection tokens (Self-RAG); complexity classifier (Adaptive-RAG) | RL policy decides mid-reasoning (Search-R1); difficulty-aware (UR²); corpus statistics (QuCo-RAG) |
| **What** to retrieve | the question | query rewriting, HyDE, decomposition (Self-Ask, IRCoT) | learned sub-queries (Search-R1); triplet placeholders (T²RAG); **latent query vectors** (LatentRAG) |
| **How much** | fixed top-k | reranking, compression | learned stopping depth (AutoSearch); cost-aware hops (RAG-on-a-Diet) |
| **How to use** it | concatenate | Chain-of-Note, RECOMP | trained working memory (State-Aware RAG); proxy policies (SPARKLE, s3) |
| **At what cost** | ignored | caching (RAGCache) | latent reasoning (LatentRAG); speculative cache repair (SpecCache) |

## Four questions to organise everything

Every paper in this repo answers at least one of:

1. **When** should the model retrieve?
2. **What** should it retrieve, and in which representation (chunks, triplets, graphs, trees, pages, latent vectors)?
3. **How** should it use what it retrieved (read, filter, remember, verify)?
4. **At what cost** (latency, tokens, money, and risk)?

## Three standard lenses (use these instead of "RAG 1.0 → 4.0")

"RAG 1.0/2.0/3.0/4.0" is **not an established taxonomy**; it came from an informal summary. If you use it, present it as your own framing. The field's more standard split, used by the KDD 2026 tutorial (Dong et al., Meta) and by the surveys, is:

- **Modular RAG:** retrieval, reranking, compression and generation are separate, swappable modules. Most of the 2023–24 toolkit lives here.
- **Graph-enhanced RAG:** the knowledge is organised as a graph, tree or other structure (GraphRAG, HippoRAG, RAPTOR, LightRAG; T²RAG and HiKEY in 2026).
- **Agentic RAG / deep research:** an LLM agent plans, retrieves over multiple turns, reflects and synthesises. It is usually trained with RL (Search-R1 onward), and at the extreme it produces long research reports.

The SoK on agentic RAG ([arXiv:2603.07379](https://arxiv.org/abs/2603.07379)) formalises agentic loops as **finite-horizon POMDPs** and classifies systems by *planning mechanism*, *retrieval orchestration*, *memory paradigm* and *tool-invocation behaviour*.

## Timeline

```
2020  RAG (Lewis) · REALM · DPR · FiD
2021  RETRO · ColBERT/SPLADE maturity
2022  Atlas · Self-Ask · IRCoT
2023  FLARE · Self-RAG · HyDE · Lost-in-the-Middle · RAGAS · ALCE
2024  CRAG · Adaptive-RAG · DRAGIN · GraphRAG · HippoRAG · RAPTOR · LightRAG
      ColPali · VisRAG · RAGCache · CacheBlend · PoisonedRAG · CRAG benchmark · FRAMES
2025  DeepSeek-R1 (Jan) → Search-o1 · R1-Searcher · Search-R1 · ReSearch · DeepResearcher
      WebThinker · ZeroSearch · s3 · HippoRAG 2 · CLaRa · deep-research agents
2026  ACL 2026: UR² · HiKEY · HiGoE · SPARKLE · SpecCache · Chart-MRAG · RAG-on-a-Diet
                Retrieval Bottleneck (main) · AutoSearch · QuCo-RAG · T²RAG
                State-Aware RAG · FRANQ · QueryLink · EgoMemory (Findings)
      arXiv:    LatentRAG · SoK Agentic RAG
      KDD 2026: tutorial "RAG: From Modular to Agentic Systems"
```

## The running example

All docs and the [code](../code/) use one question:

> **Are the directors of *Move* (1970) and *Méditerranée* (1963) from the same country?**

It is a 2WikiMultihopQA-style comparison question (also the example in the State-Aware RAG paper's Figure 1) that needs four hops:

1. *Move* (1970) → directed by **Stuart Rosenberg**
2. *Méditerranée* (1963) → directed by **Jean-Daniel Pollet**
3. Rosenberg → **American**
4. Pollet → **French** → answer: **no**

Watch how each method handles it:
- **Naive RAG** retrieves the two film pages and misses the nationalities.
- **IRCoT** gets there, but spends tokens on long chain-of-thought text.
- **Search-R1** learns to issue four searches.
- **AutoSearch** learns not to issue a fifth.
- **QuCo-RAG** notices that "Méditerranée (1963)" is rare in the pre-training corpus and retrieves before generating.
- **T²RAG** writes it as `(Move, directed by, ?d1)`, `(?d1, nationality, ?c1)`, … and resolves it in two rounds.
- **State-Aware RAG** keeps only "Rosenberg: American; Pollet: French" in working memory.
- **LatentRAG** does all four hops without decoding a single query.

## Where to go next

- New to RAG: [01 Foundations](01-foundations.md) → [02 Failure modes](02-failure-modes.md)
- Know RAG, want the frontier: [04 Learned retrieval policies](04-learned-retrieval-policies.md)
- Teaching it: [lecture-outline.md](lecture-outline.md)
