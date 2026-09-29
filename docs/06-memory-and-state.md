# 6. Memory and state

Iterative RAG accumulates context. **Memory** is the question of what to *keep*, in what form, and how to find it again. In 2026 this splits into two lines: **working memory within a reasoning episode** and **long-term memory across episodes**.

## 6.1 Working memory within an episode: State-Aware RAG (Findings ACL 2026)

Deep-dive: [papers/2026/state-aware-rag.md](../papers/2026/state-aware-rag.md)

- **Diagnosis:** prior work optimises *information acquisition* (better queries, more hops) and ignores *information management*. Retrieved text is appended, so noise accumulates.
- **Design:** an explicit working memory updated after every hop by a trained **extractor** (Qwen3-4B) that filters, consolidates and updates it. The retriever (Qwen3-Embedding-4B) and generator (Qwen3-8B) stay **frozen**.
- **Training:** SFT on about 10K successful trajectories, then GRPO with the **Path-Outcome Dual Reward**. The path reward (LLM-judge) scores whether memory is coherent and sufficient at each step; the outcome reward scores the final answer.
- **Inference:** Socratic (one chain) or MCTS (a tree with shared global memory).
- **Result:** multi-hop average 58.0% (+8.6% over HippoRAG 2); single-hop 72.7% (+9.3% over s3).

On the running example, memory after hop 4 is just:
`Move (1970) → Stuart Rosenberg (American); Méditerranée (1963) → Jean-Daniel Pollet (French)`.
The Rosenberg-surname page, the Netflix *Move* page and the 1963-festivals page never reach the generator.

## 6.2 Long-term memory across sessions

Agent memory is retrieval over the agent's own history.

| System | Idea | Link |
|---|---|---|
| **MemoRAG** (2024) | a global compressed memory model drafts clues that guide retrieval | [arXiv:2409.05591](https://arxiv.org/abs/2409.05591) · 💻 [qhjqhj00/MemoRAG](https://github.com/qhjqhj00/MemoRAG) |
| **A-MEM** (2025) | Zettelkasten-style agentic memory: notes that link and evolve | [arXiv:2502.12110](https://arxiv.org/abs/2502.12110) · 💻 [agiresearch/A-mem](https://github.com/agiresearch/A-mem) |
| **Mem0** (2025) | production memory layer: extract, update and retrieve facts | 💻 [mem0ai/mem0](https://github.com/mem0ai/mem0) |
| **QueryLink** (Findings ACL 2026) | multi-view **query–memory alignment** into a shared space + coherent memory chunking; ≥7% on LoCoMo and LongMemEval, >6% F1 on top of A-MEM | [note](../papers/2026/querylink.md) · 💻 [code](https://github.com/Dontplay0112/querylink) |
| **EgoMemory** (Findings ACL 2026) | personalised retrieval from **egocentric video**; training-free EgoRetriever (MLLM + reflective CoT); a new benchmark of 245 videos, 45 participants and 639 queries | [note](../papers/2026/egomemory.md) |

**Benchmarks:** LoCoMo ([arXiv:2402.17753](https://arxiv.org/abs/2402.17753)) and LongMemEval ([arXiv:2410.10813](https://arxiv.org/abs/2410.10813)) for conversational memory; EgoLife, EgoCVR and EgoMemory for video.

## 6.3 Themes
1. **Train the manager, freeze the rest.** State-Aware RAG (extractor), SPARKLE (proxy) and s3 (searcher) all train a small component and keep the big ones frozen, which gives plug-and-play upgrades.
2. **The query–memory gap is the old vocabulary-mismatch problem.** QueryLink's alignment is HyDE-like reasoning applied to memories.
3. **Memory is an attack surface.** The SoK on agentic RAG lists *memory poisoning* as a systemic risk (see [08](08-evidence-and-trust.md)).
