# 7. Knowledge representation: what is the unit of retrieval?

> **Code:** [`code/ragkit/t2rag.py`](../code/ragkit/t2rag.py), `python code/examples/04_t2rag.py`

The retrievable unit decides what can be found at all.

| Unit | Example systems | Strength | Weakness |
|---|---|---|---|
| Fixed chunk | DPR, Search-R1 | simple | compression loss; splits facts |
| Proposition / triplet | Dense X Retrieval, **T²RAG**, SPARKLE (for integration) | precise, composable | loses context; extraction errors |
| Entity graph | GraphRAG, HippoRAG, LightRAG | multi-hop associations | expensive to build; hub nodes |
| Induced tree | RAPTOR | multiple granularities | clustering may not match meaning |
| **Parsed document tree** | **HiKEY** | uses the author's own structure | needs good layout parsing |
| **Proposition–evidence graph** | **HiGoE** | deduplicated claims for summaries | GNN training; task-specific |
| Page image | ColPali, VisRAG, M3DocRAG | keeps layout, charts, tables | token-heavy; noisy |
| Latent vector | LatentRAG, CLaRa | fast | opaque |

## 7.1 T²RAG: triplets without a graph (Findings ACL 2026)

Deep-dive: [papers/2026/t2rag.md](../papers/2026/t2rag.md)

**Insight:** graph RAG's value comes from *fine-grained facts* and *structured multi-hop reasoning*. Its cost comes from *building the graph*. T²RAG keeps the first two and drops the third:
- **Index:** a flat vector index of verbalised triplets, with pointers to source chunks.
- **Query:** the LLM writes the question as triplets with `?` placeholders. The *question* carries the graph structure.

```
(Move (1970), directed by, ?d1)        searchable  ─┐ round 1
(Méditerranée (1963), directed by, ?d2) searchable ─┘
(?d1, nationality, ?c1)                 fuzzy → searchable once ?d1 is bound ─┐ round 2
(?d2, nationality, ?c2)                 fuzzy → searchable once ?d2 is bound ─┘
```

Results: up to +11% average over multi-round and graph RAG; about −45% retrieval-stage tokens versus IRCoT; 69.3 EM on 2Wiki with Gemini-2.5-flash.

## 7.2 HiKEY: the document's own tree (ACL 2026 main)

Deep-dive: [papers/2026/hikey.md](../papers/2026/hikey.md)

For enterprise PDFs, the structure is already there: title › section › subsection › table. HiKEY parses it with an LVLM, routes from **document to section to unit** with hybrid text and visual scoring, and packs evidence with its **governing headers** plus **sibling units** under a token budget. FRAMES "All" (every gold document retrieved) improves by +11.4 points.

## 7.3 HiGoE: evidence graphs for summarization (ACL 2026 main)

Note: [papers/2026/higoe.md](../papers/2026/higoe.md)

For long-context **summarization**, not QA: build a filtered proposition–evidence graph, organise it hierarchically with Personalized PageRank, and select evidence with an enhanced GAT. Code: [tkw123/HiGOE](https://github.com/tkw123/HiGOE).

## 7.4 Design guidance

- **Factoid multi-hop QA over encyclopedic text:** try triplets (T²RAG) before a full graph.
- **Global sense-making questions** ("What are the themes across these 500 reports?"): GraphRAG-style community summaries.
- **Structured enterprise documents:** exploit the parsed hierarchy (HiKEY). Invest in parsing.
- **Visually rich documents:** page-image retrieval (ColPali) or hierarchical multimodal (HiKEY). See [09](09-multimodal-rag.md).
- **Always keep a pointer back to the source chunk.** Both T²RAG and HiKEY lose 20–30% or more without it.
