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

## 7.4 The 2026 graph-RAG landscape

| Paper | Status | Idea |
|---|---|---|
| **TH-RAG** | ACL 2026 main | topic → subtopic → triplet hierarchy repairs fragmented LLM-built KGs ([note](../papers/2026/th-rag.md)) |
| **ParallaxRAG** | ACL 2026 main | head-specific multi-view KG retrieval, motivated by attention-head specialisation; SOTA on WebQSP/CWQ ([note](../papers/2026/parallaxrag.md)) |
| **MegaRAG** | ACL 2026 main | multimodal KG construction, retrieval and generation ([note](../papers/2026/megarag.md)) |
| **KG-R1** | arXiv 2025 | a single RL agent that treats the KG as its environment; transfers to unseen KGs |
| **ConRAG** | arXiv 2026 | consensus across relation, entity and text views; up to +26.9% over vanilla RAG |
| **PAGE-RAG** | arXiv 2026 | a temporary query-local graph over candidates; edges are *hypotheses*, not support (the "connectivity–support gap") |
| **Co-E** | arXiv 2026 | training-free synchronised graph + text working memory |
| **MG²-RAG** | arXiv 2026 | multi-granularity multimodal graph; 43× faster construction |
| **GraphRAG-Bench** | arXiv 2025 | *when* do graphs actually help RAG? ([arXiv:2506.05690](https://arxiv.org/abs/2506.05690), 💻 [GraphRAG-Bench](https://github.com/GraphRAG-Bench/GraphRAG-Benchmark)) |

Two trends: **cheaper graphs** (T²RAG drops the graph; MG²-RAG and TH-RAG lower the build cost), and **graphs as temporary reasoning scaffolds** rather than permanent indexes (PAGE-RAG, Co-E).

Toy code: [`code/ragkit/graph.py`](../code/ragkit/graph.py) (triplet graph + PPR), [`raptor.py`](../code/ragkit/raptor.py) (induced tree), [`t2rag.py`](../code/ragkit/t2rag.py) (graph-free triplets). Examples 04 and 05 solve the running example with T²RAG and PPR.

## 7.5 Design guidance

- **Factoid multi-hop QA over encyclopedic text:** try triplets (T²RAG) before a full graph.
- **Global sense-making questions** ("What are the themes across these 500 reports?"): GraphRAG-style community summaries.
- **Structured enterprise documents:** exploit the parsed hierarchy (HiKEY). Invest in parsing.
- **Visually rich documents:** page-image retrieval (ColPali) or hierarchical multimodal (HiKEY). See [09](09-multimodal-rag.md).
- **Always keep a pointer back to the source chunk.** Both T²RAG and HiKEY lose 20–30% or more without it.
