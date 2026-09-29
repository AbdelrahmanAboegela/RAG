# ParallaxRAG: "Think Parallax: Solving Multi-Hop Problems via Multi-View Knowledge-Graph-Based Retrieval-Augmented Generation"

| | |
|---|---|
| **Authors** | Jinliang Liu, Jiale Bai, Shaoning Zeng |
| **Venue / status** | **ACL 2026 main** (Long), pp. 26637–26655 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1226/) · [code](https://github.com/LucaLiu1313/ParallaxRAG) |
| **Section** | 7, Knowledge representation (KG-RAG) |
| **Verified** | Anthology abstract (September 2026) |

**Observation.** Transformer attention heads **specialise in different semantic relations at different reasoning stages**, forming a "hop-aligned relay". Standard KG-RAG embeds the query and the graph into **one** space, which flattens that structure.

**Method.** Decouple the query and the KG into **aligned, head-specific retrieval spaces** (the "multi-view"). Use them to build cleaner subgraphs and guide step-by-step reasoning.

**Results.** State of the art on **WebQSP** and **CWQ** (KGQA benchmarks), with less hallucination and strong generalisation to the biomedical domain (abstract).

**Why it's interesting.** Retrieval design here is motivated by **mechanistic interpretability** of the reader. Compare "Why RAG Fails: A Graph Perspective" (arXiv:2605.14192), which uses attribution graphs to diagnose RAG errors.
