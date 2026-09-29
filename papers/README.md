# Paper notes

One file per paper we treat in depth. Each follows [`_TEMPLATE.md`](_TEMPLATE.md): **problem → key idea → method → results → limitations → what changed → discussion questions**, and each has a **Verified** row saying what was checked against the primary source, and when.

## Status labels

Label every paper by what it is. Audiences notice the difference.

| Label | Meaning |
|---|---|
| **Other venue** | named explicitly, e.g. ICLR 2026, CCS 2026, COLM 2025 |
| **ACL 2026 main** | Long or short paper in the main ACL 2026 proceedings (`2026.acl-long.*`) |
| **Findings ACL 2026** | Findings of ACL 2026 (`2026.findings-acl.*`): peer-reviewed, not presented in the main track |
| **Workshop** | e.g. MAGMaR 2026 (`2026.magmar-main.*`) |
| **arXiv** | preprint, not peer-reviewed (yet) |

## 2026 (the frontier)

| Paper | Status | Topic | Code | Depth |
|---|---|---|---|---|
| [UR²](2026/ur2.md) | ACL 2026 main | RL: when retrieval helps, across domains | ✅ | deep-dive |
| [AutoSearch](2026/autosearch.md) | Findings ACL 2026 | RL: adaptive search depth | ✅ | deep-dive |
| [QuCo-RAG](2026/quco-rag.md) | Findings ACL 2026 | when to retrieve, from corpus statistics | ✅ | deep-dive |
| [LatentRAG](2026/latentrag.md) | arXiv (May 2026) | latent thoughts and queries, about 90% lower latency | ❌ | deep-dive |
| [State-Aware RAG](2026/state-aware-rag.md) | Findings ACL 2026 | trained working-memory curation | repo linked | deep-dive |
| [T²RAG](2026/t2rag.md) | Findings ACL 2026 | graph-free triplet RAG | ✅ | deep-dive |
| [HiKEY](2026/hikey.md) | ACL 2026 main | hierarchical multimodal document retrieval | ❌ | deep-dive |
| [SPARKLE](2026/sparkle.md) | ACL 2026 main | plug-and-play RL retrieval proxy | ✅ | short |
| [RAG-on-a-Diet](2026/rag-on-a-diet.md) | ACL 2026 main | cost-aware model choice per hop | ❌ | short |
| [The Retrieval Bottleneck](2026/retrieval-bottleneck.md) | ACL 2026 main | RL scaling laws for RAG | ❌ | short |
| [HiGoE](2026/higoe.md) | ACL 2026 main | evidence graphs for long-context *summarization* | ✅ | short |
| [FRANQ](2026/franq.md) | Findings ACL 2026 | faithfulness-aware hallucination detection | ❌ | short |
| [Chart-MRAG](2026/chart-mrag.md) | ACL 2026 main | chart-based multimodal RAG benchmark | ✅ data | short |
| [CMC-Bench](2026/cmc-bench.md) | Workshop (MAGMaR) | image–text evidence conflicts | ❌ | short |
| [SpecCache](2026/speccache.md) | ACL 2026 main | speculative KV-cache reuse | ❌ | short |
| [QueryLink](2026/querylink.md) | Findings ACL 2026 | query–memory alignment for agents | ✅ | short |
| [EgoMemory](2026/egomemory.md) | Findings ACL 2026 | personalised egocentric-video retrieval | ❌ | short |
| [BrowseComp-Plus](2026/browsecomp-plus.md) | ACL 2026 main (per repo) | fixed-corpus deep-research benchmark | ✅ | short |
| [Agentic-R](2026/agentic-r.md) | Findings ACL 2026 | retriever trained for agentic search | ❌ | short |
| [HiPRAG](2026/hiprag.md) | ICLR 2026 | per-decision process rewards for search | ❌ | short |
| [TH-RAG](2026/th-rag.md) | ACL 2026 main | topic-hierarchical knowledge graphs | ❌ | short |
| [ParallaxRAG](2026/parallaxrag.md) | ACL 2026 main | head-specific multi-view KG-RAG | ✅ | short |
| [MegaRAG](2026/megarag.md) | ACL 2026 main | multimodal KG-based RAG | ❌ | short |
| [InceptionRAG](2026/inceptionrag.md) | CCS 2026 | split-payload reasoning-based poisoning | ❌ | short |
| [OpenResearcher](2026/openresearcher.md) | arXiv (March 2026) | offline deep-research trajectory synthesis | ✅ | short |

**More 2026 work** (about 25 papers, mostly arXiv: CIPO, AgenticRag-R1, Critic-R, PAGE-RAG, ConRAG, Co-E, RGLT, EvoEmbedding, CoRM-RAG, attribution graphs, Chain of Evidence, SimpleSearch-VL, PCR, GroundedCache, FinCacheServe, SLOT, TRACE, SpliceLeak, Legal RAG Bench, enterprise AgenticRAG, Goal-Mem, and the deep-research benchmarks) is summarised in the **[2026 catalogue](2026/README.md)**.

The machine-readable index of every paper with a note is [`data/papers.csv`](../data/papers.csv), checked by `python tools/validate_papers.py`.

## 2025 (the RL-for-search turn)

- [Search-R1](2025/search-r1.md): full note. It is the bridge paper.
- [2025 catalogue](2025/README.md): about 25 systems. Search-o1, R1-Searcher, ReSearch, DeepResearcher, WebThinker, ZeroSearch, s3, DeepRAG, AutoRefine, StepSearch, R3-RAG, MaskSearch, ReARTeR, REX-RAG, KG-R1, Memory-R1, the WebWalker / WebDancer / WebSailor line, ManuSearch, R3, ReasonIR, Rank1, Tongyi DeepResearch and CLaRa, plus the weaknesses the 2026 papers attack.

## Foundations (2017–2024)

- Full notes: [Self-RAG](foundations/self-rag.md) · [GraphRAG](foundations/graphrag.md) · [HippoRAG and HippoRAG 2](foundations/hipporag.md) · [RAPTOR](foundations/raptor.md).
- [Foundations catalogue](foundations/README.md): RAG, REALM, FiD, RETRO, Atlas, DPR, ColBERT, SPLADE, HyDE, Lost-in-the-Middle, PoisonedRAG, Self-RAG, CRAG, FLARE, IRCoT, DRAGIN, Adaptive-RAG, RAPTOR, GraphRAG, HippoRAG, LightRAG, compression methods, and the surveys.

## Adding a paper

Copy `_TEMPLATE.md`, fill in every section, and fill the **Verified** row honestly: say what you read (abstract, full text, or code) and when. See [CONTRIBUTING.md](../CONTRIBUTING.md).
