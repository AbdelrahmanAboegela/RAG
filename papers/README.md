# Paper notes

One file per paper we treat in depth. Each follows [`_TEMPLATE.md`](_TEMPLATE.md): **problem → key idea → method → results → limitations → what changed → discussion questions**, and each has a **Verified** row saying what was checked against the primary source, and when.

## Status labels

Label every paper by what it is. Audiences notice the difference.

| Label | Meaning |
|---|---|
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

## 2025 (the RL-for-search turn)

- [Search-R1](2025/search-r1.md): full note. It is the bridge paper.
- [2025 catalogue](2025/README.md): Search-o1, R1-Searcher, ReSearch, DeepResearcher, WebThinker, ZeroSearch, s3, Tongyi DeepResearch, CLaRa, and the weaknesses the 2026 papers attack.

## Foundations (2017–2024)

- [Foundations catalogue](foundations/README.md): RAG, REALM, FiD, RETRO, Atlas, DPR, ColBERT, SPLADE, HyDE, Lost-in-the-Middle, PoisonedRAG, Self-RAG, CRAG, FLARE, IRCoT, DRAGIN, Adaptive-RAG, RAPTOR, GraphRAG, HippoRAG, LightRAG, compression methods, and the surveys.

## Adding a paper

Copy `_TEMPLATE.md`, fill in every section, and fill the **Verified** row honestly: say what you read (abstract, full text, or code) and when. See [CONTRIBUTING.md](../CONTRIBUTING.md).
