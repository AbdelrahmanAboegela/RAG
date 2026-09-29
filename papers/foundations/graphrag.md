# GraphRAG: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"

| | |
|---|---|
| **Authors** | Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, Jonathan Larson (Microsoft) |
| **Venue / status** | arXiv April 2024 (Microsoft Research) |
| **Links** | [arXiv:2404.16130](https://arxiv.org/abs/2404.16130) · [code](https://github.com/microsoft/graphrag) · lighter re-implementations: [nano-graphrag](https://github.com/gusye1234/nano-graphrag), [LightRAG](https://github.com/HKUDS/LightRAG) |
| **Section** | 3 and 7, Structured knowledge |

## TL;DR
Answer **global** questions about a whole corpus ("What are the main themes?") by building an entity graph, clustering it into communities, pre-summarising each community, and then map-reducing over the summaries.

## 1. Problem
Vector RAG retrieves the top-k *local* chunks. It cannot answer questions whose answer is spread across the **whole** corpus. That is query-focused summarization, not needle-finding.

## 2. Method
**Indexing (offline, LLM-heavy)**
1. Chunk the corpus, then have an LLM extract **entities, relations and claims** from each chunk (with "gleaning" passes to catch misses).
2. Build the graph and summarise each entity and relation.
3. Detect communities hierarchically with **Leiden**.
4. Have the LLM write a **report for every community** at every level.

**Query**
- **Global search (map-reduce):** each community report produces a partial answer with a helpfulness score (map). The top partial answers are combined into the final answer (reduce).
- **Local search** (added in the codebase): start from entities linked to the query and gather their neighbourhood, related chunks and community context.

## 3. Results
On global sense-making questions over podcast transcripts and news (about 1M tokens each), GraphRAG beat vector RAG on **comprehensiveness and diversity**, judged by an LLM in head-to-head comparisons.

## 4. Limitations
- **Indexing cost:** many LLM calls per chunk. This is the cost that LightRAG, T²RAG (graph-free) and MG²-RAG (43× faster builds) react to.
- **Evaluation:** LLM-judged, on *global* questions. On factoid multi-hop QA it is often not better than vector RAG; GraphRAG-Bench ([arXiv:2506.05690](https://arxiv.org/abs/2506.05690)) studies when graphs actually help.
- **Updates:** incremental indexing is hard.

## 5. What changed
It made "graph RAG" mainstream and separated **local** (needle) from **global** (sense-making) questions, a distinction every RAG design should make first.
