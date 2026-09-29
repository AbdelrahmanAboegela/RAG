# 3. The toolkit you need first (2022–2024)

Before RL-trained search agents, "advanced RAG" meant a set of mostly prompt-based or supervised techniques. The 2026 papers use them as baselines and building blocks. Full per-paper entries, with links and code, are in [papers/foundations](../papers/foundations/README.md).

## 3.1 Iterative and interleaved retrieval

| Method | When to retrieve | What query | Learned? |
|---|---|---|---|
| **Self-Ask** (2022) | whenever the model asks a follow-up | the follow-up question | prompted |
| **IRCoT** (2022/23) | after every CoT sentence | the CoT sentence | prompted |
| **ReAct** (2022/23) | when the model emits an action | the action argument | prompted |
| **FLARE** (2023) | when a token in the draft sentence has low probability | the draft sentence, uncertain tokens masked | prompted + threshold |
| **DRAGIN** (2024) | uncertainty × attention importance | built from attention over context | prompted + threshold |
| **Self-RAG** (2023/24) | when the model emits `[Retrieve]` | the current segment | **supervised** (GPT-4-distilled reflection labels) |
| **Adaptive-RAG** (2024) | per query, by a complexity classifier | none / single / multi-step | **supervised** classifier |

**Pattern:** the decision rules are *hand-designed* (thresholds, prompts) or *imitated* (labels). Section 4 is what happens when they are *optimised for the outcome*.

## 3.2 Corrective and robust reading

- **CRAG (Corrective RAG):** a lightweight evaluator labels retrieval Correct, Incorrect or Ambiguous. It triggers web search as a fallback and filters through decompose-then-recompose.
- **Chain-of-Note:** write a note per document ("relevant? what does it say?") before answering.
- **RECOMP, LongLLMLingua:** compress context before reading.
- **Speculative RAG:** a small drafter works on document subsets in parallel, and a large verifier checks the drafts.

## 3.3 Structured knowledge: graphs and trees

| Method | Structure | Built by | Retrieval | Best for |
|---|---|---|---|---|
| **GraphRAG** (Microsoft) | entity–relation graph + community summaries | LLM extraction + Leiden clustering | map-reduce over community summaries | *global* sense-making questions |
| **HippoRAG / 2** | OpenIE KG (+ passage nodes in v2) | LLM OpenIE | Personalized PageRank from query entities | multi-hop associative QA |
| **LightRAG** | entity + theme graph | LLM extraction, incremental | dual-level (local and global) | cheap graph RAG in practice |
| **RAPTOR** | tree of recursive cluster summaries | GMM clustering + LLM summaries | across tree levels | long documents, multi-granularity |

**Their shared cost:** building the structure needs an LLM pass over the whole corpus, sometimes several. Their shared risk: extraction errors and hub nodes. **2026 responses:** T²RAG (keep triplets, drop the graph), HiKEY (use the document's *own* hierarchy), HiGoE (a proposition–evidence graph for summarization).

## 3.4 What to take from this section

1. **Iterative retrieval works.** IRCoT remains a strong baseline in 2026 papers.
2. **Uncertainty-triggered retrieval is fragile**, because LLM confidence is poorly calibrated. QuCo-RAG's starting point.
3. **Supervised retrieval policies are capped by their labels.** Search-R1's starting point.
4. **Structure helps multi-hop, but it is expensive to build.** T²RAG's starting point.

## Slides tip
Show the running example through IRCoT: each CoT sentence becomes a query. Then ask the audience: *who decided that every sentence should trigger a search?* That question leads into Section 4.
