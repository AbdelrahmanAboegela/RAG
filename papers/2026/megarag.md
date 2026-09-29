# MegaRAG: Multimodal Knowledge Graph-Based Retrieval Augmented Generation

| | |
|---|---|
| **Authors** | Chi-Hsiang Hsiao, Yi-Cheng Wang, Tzung-Sheng Lin, Yi-Ren Yeh, Chu-song Chen |
| **Venue / status** | **ACL 2026 main** (Long), pp. 48031–48059 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.2218/) |
| **Section** | 9, Multimodal / 7, Graph RAG |
| **Verified** | Anthology abstract (September 2026) |

**Problem.** Graph RAG (GraphRAG, LightRAG) builds knowledge graphs from **text only**, so figures, diagrams and page images in a document never enter the graph.

**Method.** Integrate **visual information** into all three stages: **KG construction** (multimodal entities and relations), **retrieval**, and **answer generation**.

**Result.** Improvements on both textual and multimodal QA benchmarks (abstract).

**Related 2026 work.** MG²-RAG ([arXiv:2604.04969](https://arxiv.org/abs/2604.04969)) builds a multi-granularity multimodal graph that fuses text entities with grounded visual regions. It reports a 43.3× faster and 23.9× cheaper graph build than advanced graph-based frameworks. See [docs/09](../../docs/09-multimodal-rag.md).
