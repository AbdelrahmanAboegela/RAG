# HippoRAG (NeurIPS 2024) and HippoRAG 2 (ICML 2025)

| | |
|---|---|
| **Authors** | HippoRAG: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su. HippoRAG 2: Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, Yu Su (OSU) |
| **Venue / status** | **NeurIPS 2024**; HippoRAG 2 ("From RAG to Memory: Non-Parametric Continual Learning for LLMs") **ICML 2025** |
| **Links** | [arXiv:2405.14831](https://arxiv.org/abs/2405.14831) · [arXiv:2502.14802](https://arxiv.org/abs/2502.14802) · [code](https://github.com/OSU-NLP-Group/HippoRAG) · toy PPR: [`code/ragkit/graph.py`](../../code/ragkit/graph.py) |
| **Section** | 3, 6, 7 |

## TL;DR
Model long-term memory after the **hippocampal indexing theory**. The LLM is the neocortex (it extracts and reasons), an OpenIE knowledge graph is the hippocampal index (it associates), and **Personalized PageRank** does pattern completion from the query's entities. This gives multi-hop retrieval in a *single* step.

## Method (HippoRAG)
1. **Offline indexing:** an LLM runs OpenIE on every passage to get (subject, relation, object) triples. Build a schemaless KG, and add *synonymy edges* between entities whose embeddings are close.
2. **Online retrieval:**
   - The LLM extracts named entities from the query and links them to KG nodes by embedding similarity.
   - Run **PPR** seeded at those nodes, with node weights down-weighted by node specificity (an IDF-like term).
   - Score each passage by the PPR mass of its entities, and return the top passages.
3. There is no iteration, yet PPR mass flows 2–3 hops. Run `python code/examples/05_graph_ppr.py` to see it reach both nationality passages of the running example.

## Results (HippoRAG)
Large gains over dense retrievers on 2Wiki and MuSiQue, comparable to or better than IRCoT at a fraction of the cost. IRCoT + HippoRAG is complementary.

## HippoRAG 2
- Adds **passage nodes** to the graph (dense-sparse integration), so PPR ranks passages directly.
- Matches queries to **triples**, not just entities, and adds LLM **recognition-memory filtering** of the retrieved triples.
- Better on factual, sense-making *and* associative memory tasks. HippoRAG 1 had regressed on simple factual QA compared with strong dense retrievers.

## Why it matters in 2026
- **State-Aware RAG** uses HippoRAG 2 as its strongest *memory-augmented* baseline (+8.6% over it).
- **T²RAG** includes a `hippo` baseline in its codebase.
- PPR reappears in **HiGoE** (ACL 2026).

## Limitations
OpenIE cost and errors, entity-linking errors, and a **static** graph that does not adapt to the evolving reasoning state, which is State-Aware RAG's critique.
