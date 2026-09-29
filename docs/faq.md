# FAQ

**Is RAG dead now that context windows hold a million tokens?**
No. Long context often wins on average quality when cost is no object, but RAG is far cheaper, supports freshness and access control, and gives citations. Hybrids (routing, LongRAG-style long units) are common. See [14](14-long-context-vs-rag.md).

**What's the single most effective improvement to a basic RAG system?**
Usually a **reranker** on top of **hybrid (BM25 + dense) retrieval**, after fixing parsing and chunking. Measure recall first. See [17](17-production-guide.md).

**Should I use GraphRAG?**
Use it for *global* sense-making questions over a corpus ("main themes across these reports"). For factoid multi-hop QA, try iterative retrieval or triplet-based methods (T²RAG) first. GraphRAG-Bench studies when graphs help. See [07](07-knowledge-representation.md).

**Do I need RL to get agentic RAG?**
No. A prompted agent with search/open/find tools over your existing search is a strong baseline (AgenticRAG, 2026). RL (Search-R1, UR², AutoSearch) pays off when you train a small open model to act as the agent, or need efficiency (fewer searches). See [04](04-learned-retrieval-policies.md).

**Which RL algorithm: PPO or GRPO?**
Both are used. GRPO needs no critic and is cheaper; PPO is often more stable for sparse rewards. Most gains in 2026 papers come from **reward design** (process, efficiency, evidence-use) and **retrieval quality**, not the algorithm (The Retrieval Bottleneck). See [`code/ragkit/rl.py`](../code/ragkit/rl.py).

**Why do papers report such different numbers on HotpotQA?**
Different backbones, retrievers, corpora, sample sizes, metrics and baselines. Don't compare across papers. See [11](11-evaluation.md).

**How do I know when retrieval is needed?**
Options: model uncertainty (FLARE/DRAGIN; unreliable), a learned router (Adaptive-RAG), corpus statistics (QuCo-RAG), or an RL policy that learns it (Search-R1, UR², HiPRAG). See [04](04-learned-retrieval-policies.md).

**Are multimodal documents (charts, tables) solved?**
No. Even with gold retrieval, the best MLLMs reach about 71% correctness on Chart-MRAG, and models are biased toward text. See [09](09-multimodal-rag.md).

**How do I protect a RAG system from poisoning?**
There is no complete defense. Control corpus writes, keep provenance, retrieve wider and filter, isolate documents, treat retrieved text as data, and red-team. See [15](15-security.md).

**Is caching answers safe?**
Only with gates: evidence overlap, source-version checks and support in fresh evidence (GroundedCache), scoped per tenant. See [10](10-efficiency.md) and [`cache.py`](../code/ragkit/cache.py).

**What is "RAG 1.0 → 4.0"?**
An informal framing, not an established taxonomy. The standard split is modular / graph-enhanced / agentic (plus deep research). See [00](00-overview.md).

**Where do I start reading?**
[reading-list.md](reading-list.md). The one-paper-per-era path: Lewis et al. 2020 → Self-RAG → Search-R1 → UR² → LatentRAG.
