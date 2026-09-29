# Glossary

| Term | Meaning | Where |
|---|---|---|
| **Adaptive retrieval** | deciding per query or per step whether to retrieve at all | FLARE, DRAGIN, Adaptive-RAG, UR², QuCo-RAG |
| **Agentic RAG** | an LLM agent decides when and what to retrieve over multiple turns, usually via tool calls | [04](04-learned-retrieval-policies.md) |
| **All@k** | 1 if *every* gold passage is in the top k; stricter than recall for multi-hop | HiKEY; [`evaluate.py`](../code/ragkit/evaluate.py) |
| **ANN** | approximate nearest-neighbour search (HNSW, IVF, PQ) over embeddings | FAISS |
| **BM25** | sparse lexical ranking function with TF saturation and length normalisation | [01](01-foundations.md) |
| **Bi-encoder** | embeds query and document separately; fast, precomputable | DPR, E5 |
| **Chunk** | the unit a document is split into for indexing | [01](01-foundations.md) |
| **Collapsed tree** | RAPTOR retrieval over all tree levels at once | RAPTOR |
| **Context engineering** | optimising everything placed in the context window: retrieval, memory, tools, instructions | [14](14-long-context-vs-rag.md) |
| **Cover-EM** | 1 if a gold answer string is contained in the prediction | [11](11-evaluation.md) |
| **Cross-encoder** | scores query and document jointly; accurate, slow; used for reranking | [01](01-foundations.md) |
| **Deep research** | long-horizon agent producing cited reports from many searches | [13](13-deep-research.md) |
| **EM / F1** | exact match / token-overlap F1 after SQuAD normalisation | [`metrics.py`](../code/ragkit/metrics.py) |
| **Faithfulness** | whether a claim is supported by the retrieved context (≠ factuality) | FRANQ |
| **GRPO** | Group Relative Policy Optimization: advantage = reward minus group mean, divided by group std; no critic | [`rl.py`](../code/ragkit/rl.py) |
| **Hard negative** | a passage that looks relevant but doesn't answer; hurts readers, helps retriever training | ReasonIR |
| **HyDE** | retrieve with the embedding of a generated hypothetical answer | [01](01-foundations.md) |
| **Hybrid retrieval** | sparse + dense, usually fused with RRF | [`rrf_hybrid.py`](../code/ragkit/rrf_hybrid.py) |
| **Indirect prompt injection** | instructions hidden in retrieved content | [15](15-security.md) |
| **Infini-gram** | suffix-array engine for n-gram counts over trillion-token corpora | QuCo-RAG |
| **KV cache** | stored attention keys/values; reusing it skips prefill | [10](10-efficiency.md) |
| **Late interaction** | token-level embeddings scored with MaxSim | ColBERT, ColPali |
| **Latent retrieval** | the query is a hidden-state vector, not text | LatentRAG |
| **Lost in the middle** | LLMs use the start and end of the context better than the middle | [02](02-failure-modes.md) |
| **Minimal sufficient search depth** | first step at which the agent's intermediate answer is correct | AutoSearch |
| **MMR** | Maximal Marginal Relevance: relevance minus redundancy | [`rerank.py`](../code/ragkit/rerank.py) |
| **Multi-hop QA** | answering needs chaining facts from several documents | HotpotQA, 2Wiki, MuSiQue |
| **OpenIE** | open information extraction of (subject, relation, object) triplets | HippoRAG, T²RAG |
| **Over-/under-search** | searching when unnecessary / not searching when necessary | AutoSearch, HiPRAG |
| **PPO** | Proximal Policy Optimization: clipped policy-gradient objective with a value critic | Search-R1 |
| **PPR** | Personalized PageRank: random walk restarting at seed nodes | HippoRAG; [`graph.py`](../code/ragkit/graph.py) |
| **Prefill / TTFT** | processing the prompt before generating / time-to-first-token | [10](10-efficiency.md) |
| **Process reward** | reward for intermediate steps rather than only the final answer | StepSearch, HiPRAG, State-Aware RAG |
| **Proposition** | an atomic, self-contained factoid used as a retrieval unit | Dense X Retrieval |
| **Query decomposition** | splitting a question into sub-questions | Self-Ask, T²RAG |
| **Reflection tokens** | special tokens that let a model gate retrieval and critique itself | Self-RAG |
| **Retrieved-token masking** | excluding retriever-inserted tokens from the RL loss | Search-R1; [`rl.py`](../code/ragkit/rl.py) |
| **RRF** | Reciprocal Rank Fusion: Σ 1/(k + rank) | [`fusion.py`](../code/ragkit/fusion.py) |
| **Self-answering** | agent emits an intermediate answer after each search | AutoSearch |
| **Speculative (model)** | a small model's output guides or pre-computes for a large one | Speculative RAG, SpecCache |
| **Working memory** | curated, persistent state updated each reasoning step | State-Aware RAG |
