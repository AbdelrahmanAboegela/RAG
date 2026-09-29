# 18. Retrievers for reasoning and for agents

Sections 4–6 mostly train the **policy** and keep the retriever fixed. But The Retrieval Bottleneck (ACL 2026), BrowseComp-Plus, State-Aware RAG and Legal RAG Bench all point the same way: **the retriever sets the ceiling**. This chapter covers the 2025–26 work that improves the *retriever* for reasoning-heavy and agentic use.

## 18.1 Why classic retrievers fall short

| Classic assumption | Agentic / reasoning reality |
|---|---|
| Queries are short human questions | queries are **agent-written sub-queries**, often mid-reasoning |
| Relevance = topical similarity | usefulness = *does this passage advance the next reasoning step?* (the KDD 2026 tutorial's point: relevance correlates weakly with downstream quality; informativeness matters) |
| One query → one ranked list | many turns; the value of a passage depends on what is already known |
| Most similar = best | the most relevant evidence can be **sycophantic** to a biased query (CoRM-RAG) |

## 18.2 Retrievers trained for reasoning

| Model | Idea | Result | Link |
|---|---|---|---|
| **ReasonIR-8B** (2025) | synthetic hard queries + plausible-but-unhelpful hard negatives per document | BRIGHT 29.9 / 36.9 nDCG@10 (without / with reranker); +22.6% GPQA in RAG | [arXiv:2504.20595](https://arxiv.org/abs/2504.20595) · 💻 [facebookresearch/ReasonIR](https://github.com/facebookresearch/ReasonIR) |
| **Rank1** (CoLM 2025) | reranker that *reasons* (test-time compute), distilled from 600K+ R1 traces | strong on reasoning and instruction-following reranking; explainable | [arXiv:2502.18418](https://arxiv.org/abs/2502.18418) · 💻 [orionw/rank1](https://github.com/orionw/rank1) |
| **RGLT** (2026) | latent "silent-token" reasoning inside the embedder; each latent step supervised to raise retrieval quality | beats reasoning-enhanced embedders on reasoning-intensive retrieval | [arXiv:2608.14107](https://arxiv.org/abs/2608.14107) |
| **EvoEmbedding** (2026) | **evolvable** embeddings: recurrent latent memory over a long context, so the same query retrieves different targets as the context changes | outperforms larger static embedders on long-context retrieval; naive RAG + EvoEmbedding beats agentic memory systems | [arXiv:2606.21649](https://arxiv.org/abs/2606.21649) |

Benchmark: **BRIGHT** ([arXiv:2407.12883](https://arxiv.org/abs/2407.12883)), for reasoning-intensive retrieval.

## 18.3 Retrievers trained *for the agent*

| Method | Training signal | Link |
|---|---|---|
| **R3** (2025) | RL on the retriever inside a RAG environment; +5.2% over the original retriever; 4 GPUs, one day | [arXiv:2510.24652](https://arxiv.org/abs/2510.24652) |
| **Agentic-R** (Findings ACL 2026) | local query–passage relevance + global answer correctness; agent and retriever optimised **iteratively in both directions** | [note](../papers/2026/agentic-r.md) |
| **Critic-R** (2026) | a critic judges whether retrieved evidence supports the agent's next step. Inference-time query refinement (Critic-R-Zero) and retriever training from refinement trajectories (Critic-Embed), with no relevance labels | [arXiv:2606.00590](https://arxiv.org/abs/2606.00590) |
| **LatentRAG** (2026) | retriever co-trained to accept *latent* queries from the LLM | [note](../papers/2026/latentrag.md) |
| **UR²** (ACL 2026) | not the retriever itself, but LLM *summaries* of retrieved text as the knowledge interface | [note](../papers/2026/ur2.md) |

## 18.4 Robustness-aware retrieval
**CoRM-RAG** (2026, [arXiv:2605.01302](https://arxiv.org/abs/2605.01302)) trains an evidence critic under simulated **cognitive biases** (false premises, confirmation bias), so it ranks documents by their power to *correct* the model rather than their similarity to a flawed query. It also enables risk-aware abstention.

## 18.5 Practical guidance
1. Measure **retrieval recall on agent-written sub-queries**, not only on user questions. Log them from your agent.
2. Try a **reasoning reranker** (Rank1-style) before retraining the embedder. It is cheaper and often enough.
3. If you control training, the 2026 direction is **joint or iterative agent–retriever optimisation** (Agentic-R, Critic-R).
4. For long, evolving contexts such as chats and logs, static chunk embeddings miss order and state. Consider memory-aware approaches (EvoEmbedding, and QueryLink in [06](06-memory-and-state.md)).
