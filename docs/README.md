# Docs

A structured course on advanced RAG, organised around one thesis (*from engineered pipeline to learned policy*) and four questions (*when, what, how, at what cost*).

## Core course

| # | Chapter | Key papers |
|---|---|---|
| 00 | [Overview: thesis, taxonomy, landscape map, timeline, running example](00-overview.md) | — |
| 01 | [Foundations: pipeline, chunking, sparse/dense/hybrid, reranking, tooling](01-foundations.md) | DPR, BM25, ColBERT, HyDE, Rank1 |
| 02 | [Why vanilla RAG fails](02-failure-modes.md) | Lost-in-the-Middle, ClashEval, PoisonedRAG |
| 03 | [The classic advanced-RAG toolkit](03-classic-advanced-rag.md) | IRCoT, FLARE, Self-RAG, CRAG, GraphRAG, HippoRAG, RAPTOR |
| 04 | [Learned retrieval policies (RL for search)](04-learned-retrieval-policies.md) | Search-R1, **UR²**, **AutoSearch**, **QuCo-RAG**, **HiPRAG**, **SPARKLE**, **RAG-on-a-Diet**, **Retrieval Bottleneck**, **CIPO** |
| 05 | [Latent retrieval](05-latent-retrieval.md) | **LatentRAG**, CLaRa, Coconut |
| 06 | [Memory and state](06-memory-and-state.md) | **State-Aware RAG**, **QueryLink**, **EgoMemory**, Memory-R1, MemGPT |
| 07 | [Knowledge representation and graph RAG](07-knowledge-representation.md) | **T²RAG**, **HiKEY**, **HiGoE**, **TH-RAG**, **ParallaxRAG** |
| 08 | [Evidence and trust](08-evidence-and-trust.md) | **FRANQ**, **CMC-Bench** |
| 09 | [Multimodal RAG](09-multimodal-rag.md) | **Chart-MRAG**, **MegaRAG**, ColPali, VisRAG, M3DocRAG, CRAG-MM |
| 10 | [Efficiency and caching](10-efficiency.md) | **SpecCache**, RAGCache, CacheBlend, CacheClip, GroundedCache |
| 11 | [Evaluation](11-evaluation.md) | CRAG, FRAMES, **BrowseComp-Plus**, RGB, BRIGHT |
| 12 | [Open problems](12-open-problems.md) | — |

## Extended chapters

| # | Chapter | Key papers |
|---|---|---|
| 13 | [Deep research agents](13-deep-research.md) | WebSailor, **OpenResearcher**, BrowseComp-Plus, ResearchRubrics, **MiroEval** |
| 14 | [Long context vs. RAG, and context engineering](14-long-context-vs-rag.md) | Self-Route, OP-RAG, LongRAG, LaRA |
| 15 | [Security and privacy](15-security.md) | PoisonedRAG, **InceptionRAG**, **SLOT**, **SpliceLeak** |
| 16 | [Domain and enterprise RAG](16-domain-and-enterprise-rag.md) | MIRAGE, **Legal RAG Bench**, FinanceBench, **AgenticRAG**, CRAG-MM |
| 17 | [Production guide](17-production-guide.md) | engineering defaults, tools, evaluation loop |
| 18 | [Retrievers for reasoning and agents](18-retrievers-for-reasoning-and-agents.md) | ReasonIR, Rank1, **Agentic-R**, R3, **Critic-R**, **EvoEmbedding** |

Bold = 2026 papers.

## Reference
[comparison-matrix.md](comparison-matrix.md) · [glossary.md](glossary.md) · [faq.md](faq.md)

## Teaching
[lecture-outline.md](lecture-outline.md) · [reading-list.md](reading-list.md) · slide deck: [`../slides/advanced-rag.md`](../slides/advanced-rag.md)

## Trust in this repo
[verification-log.md](verification-log.md)
