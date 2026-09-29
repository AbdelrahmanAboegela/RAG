# T²RAG: "Beyond Chunks and Graphs: Retrieval-Augmented Generation through Triplet-Driven Thinking"

| | |
|---|---|
| **Authors** | Shengbo Gong, Xianfeng Tang, Qi He, Carl Yang, Wei Jin (Emory) |
| **Venue / status** | **Findings of ACL 2026**. On arXiv since August 2025 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.1310/) · [arXiv:2508.02435](https://arxiv.org/abs/2508.02435) · [code](https://github.com/Emory-Melody/T2RAG) · [reproduction guide](../../experiments/t2rag.md) · [toy loop](../../code/ragkit/t2rag.py) |
| **Section** | 7, Knowledge representation |
| **Verified** | Method and numbers from arXiv HTML (September 2026) |

## TL;DR
T²RAG uses **atomic triplets** as the retrieval unit, but does not build a graph. The LLM rewrites the question as triplets with `?` placeholders and fills them in over a few rounds of retrieval. It reports up to 11% average gains over multi-round and graph RAG, with up to 45% lower retrieval cost.

## 1. Problem and gap
- **Chunk RAG** has *compression loss*: one embedding per 100-word chunk blurs the detail needed for multi-hop questions.
- **Graph RAG** (GraphRAG, HippoRAG, LightRAG) is expensive to build (entity extraction, disambiguation, graph assembly) and suffers from *high-degree hub nodes* that pull in redundant context.
- **Iterative RAG** (IRCoT) passes long chain-of-thought text between rounds, which wastes tokens.

## 2. Key idea
Keep the *fine granularity* of a knowledge graph and drop the *graph*. Store verbalised triplets in a flat vector index, and let the **question's own structure**, expressed as triplets with variables, drive retrieval.

## 3. Method
**Indexing**
1. OpenIE extracts (subject, predicate, object) triplets from each chunk.
2. Each triplet is verbalised as a sentence and embedded with NV-Embed-v2 into a FAISS index.
3. The mapping from triplet to source chunk is kept.

**Query-time loop** (at most N=3 rounds)
1. **Decompose** the question into triplets. *Resolved* triplets have 0 placeholders, *searchable* triplets have 1, and *fuzzy* triplets have 2 or more.
2. **Adaptive retrieval:** for each searchable triplet, retrieve propositions until *k unique source chunks* are collected, rather than a fixed top-k.
3. **Resolve:** the LLM fills placeholders from the propositions and chunks.
4. **Update state:** resolved triplets become facts; newly bound variables turn fuzzy triplets into searchable ones.
5. **Stop** when no searchable or fuzzy triplets remain, when no new searchable triplet appears, or after N rounds.

Only compact triplets are passed between rounds, not free-text reasoning.

## 4. Results
- **LLMs:** Gemini-2.5-flash and GPT-4o-mini. **Datasets:** PopQA; 2Wiki, MuSiQue, HotpotQA; Story, Medical.
- **2Wiki (Gemini-2.5-flash):** 69.3 EM / 77.5 F1, +7.7 EM over IRCoT.
- **Average gain** up to 11% across the six datasets, largest on factoid EM.
- **Cost:** about 45% fewer retrieval-stage tokens than IRCoT, with latency close to single-round methods. Indexing costs more than chunk RAG, but graph RAG needs 6–10× more tokens.
- **Ablations:** single-round only drops F1 by 54.5% on MuSiQue. Removing the source chunks costs 26–34%.

## 5. Limitations
- **(stated)** Errors in triplet extraction propagate.
- **(stated)** Indexing is token-heavy at corpus scale, although adding documents incrementally is cheap.
- **(stated)** Triplets capture many-to-many relations poorly.
- **(stated)** Evaluation is factoid-only, capped at 3 iterations.
- **(stated)** It benefits most from strong reasoning LLMs.

## 6. What changed vs. the previous approach
"Graph-structured reasoning without a graph": the **query** carries the structure (placeholder triplets), so the **index** can stay a flat list.

## 7. Discussion questions
1. Why do placeholder triplets reduce the need for entity disambiguation compared with HippoRAG's graph?
2. Run [`code/examples/04_t2rag.py`](../../code/examples/04_t2rag.py). Which question types would *not* decompose cleanly into triplets?
