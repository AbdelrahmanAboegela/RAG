# TH-RAG: Topic-Based Hierarchical Knowledge Graphs for Robust Multi-hop Reasoning in Graph-based RAG Systems

| | |
|---|---|
| **Authors** | JungHyoun Kim, Soohyeong Kim, Seok Jun Hwang, Jeonghyeon Park, Yong Suk Choi |
| **Venue / status** | **ACL 2026 main** (Long), pp. 37508–37531 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1740/) |
| **Section** | 7, Knowledge representation (graph RAG) |
| **Verified** | Anthology abstract (September 2026) |

**Problem.** LLM-extracted triplet KGs are **fragmented and sparsely connected**, which breaks multi-hop paths. The usual fixes (clustering and community detection, as in GraphRAG) add compute and can merge unrelated content.

**Method.** Organise triplets into a **topic → subtopic → triplet hierarchy**. This adds connectivity through shared topics and gathers scattered facts about the same theme, without full community detection.

**Result.** Better accuracy and robustness on QA benchmarks while staying computationally efficient (abstract). Read the tables before quoting numbers.

**Where it fits.** It sits between GraphRAG (communities) and T²RAG (no graph). The hierarchy is *topical*; compare RAPTOR (clustered summaries) and HiKEY (the document's own structure).
