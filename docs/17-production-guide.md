# 17. Building RAG in production: a practical guide

This chapter turns the research into engineering defaults. Each default links to the evidence behind it. **Measure before and after every change.** None of these defaults beats an evaluation on your own data.

## 17.1 Start with the questions, not the stack
1. Collect **50–200 real user questions** with expert answers and the source passages. This is your regression test (see Legal RAG Bench: 100 questions were enough to rank systems).
2. Label each question: *needle* (one fact), *multi-hop*, *global/synthesis*, *numeric/table*, *visual*, or *no retrieval needed*. The mix decides the architecture (see the decision tree in [14](14-long-context-vs-rag.md)).

## 17.2 Default pipeline (a strong baseline before anything agentic)

| Stage | Default | Why / evidence |
|---|---|---|
| Parsing | a layout-aware parser that keeps headings, tables and reading order ([Docling](https://github.com/docling-project/docling), [MinerU](https://github.com/opendatalab/MinerU), [Marker](https://github.com/datalab-to/marker), [Unstructured](https://github.com/Unstructured-IO/unstructured)) | most downstream errors start here; HiKEY's gains come from structure |
| Chunking | structure-aware, about 200–500 tokens, keep the section path as metadata; store parent pointers | small chunks for precision, parent expansion for context (HiKEY, T²RAG keep source chunks) |
| Contextualise | prepend document title + section path (or an LLM-written situating sentence) before embedding | contextual retrieval / late chunking |
| Retrieval | **hybrid BM25 + dense**, fused with RRF, top 50–100 | robust to rare entities and paraphrase ([01](01-foundations.md)) |
| Rerank | cross-encoder or LLM reranker down to 5–10 | usually the cheapest big win |
| Ordering | best evidence first and last; MMR to deduplicate | lost-in-the-middle |
| Prompt | answer only from context, cite passage IDs, say "not found" otherwise; mark retrieved text as untrusted | ALCE; [15](15-security.md) |
| Access control | filter by user permissions **inside** the retriever | [16](16-domain-and-enterprise-rag.md) |

Toy versions of every stage are in [`code/ragkit`](../code/ragkit/).

## 17.3 When to add what

| Symptom (from your eval) | Add | See |
|---|---|---|
| Correct passage not in top-50 | better parsing/chunking, domain embedder, query rewriting/HyDE | [01](01-foundations.md), [18](18-retrievers-for-reasoning-and-agents.md) |
| Correct passage retrieved but answer wrong | reranker, fewer passages, better ordering, reader fine-tuning (InstructRAG) | [02](02-failure-modes.md) |
| Multi-hop questions fail | iterative/agentic retrieval (IRCoT → agent with search tools), or graph/triplet retrieval | [04](04-learned-retrieval-policies.md), [07](07-knowledge-representation.md) |
| "Summarise everything about X" fails | GraphRAG-style community summaries, RAPTOR, or long context | [07](07-knowledge-representation.md), [14](14-long-context-vs-rag.md) |
| Tables and charts wrong | page-image retrieval (ColPali) or structure-aware multimodal (HiKEY) | [09](09-multimodal-rag.md) |
| Too slow or expensive | routing (skip retrieval), caching (prefix/KV; safe answer cache), smaller reader | [10](10-efficiency.md) |
| Confident wrong answers | abstention thresholds, support checks (FRANQ-style), citations | [08](08-evidence-and-trust.md) |

## 17.4 Infrastructure choices

| Need | Options (all open source) |
|---|---|
| Vector index library | [FAISS](https://github.com/facebookresearch/faiss) |
| Vector databases | [Milvus](https://github.com/milvus-io/milvus), [Qdrant](https://github.com/qdrant/qdrant), [Weaviate](https://github.com/weaviate/weaviate), [Chroma](https://github.com/chroma-core/chroma), [LanceDB](https://github.com/lancedb/lancedb) |
| Search engines with hybrid (BM25 + vector) | [Elasticsearch](https://github.com/elastic/elasticsearch), [OpenSearch](https://github.com/opensearch-project/OpenSearch), [Vespa](https://github.com/vespa-engine/vespa) |
| Vectors inside Postgres | [pgvector](https://github.com/pgvector/pgvector) |
| IR research toolkit (BM25, dense, eval) | [Pyserini](https://github.com/castorini/pyserini) |
| Embedding / reranking libraries | [sentence-transformers](https://github.com/UKPLab/sentence-transformers), [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding), [RAGatouille (ColBERT)](https://github.com/AnswerDotAI/RAGatouille) |
| LLM serving with prefix caching | [vLLM](https://github.com/vllm-project/vllm), [SGLang](https://github.com/sgl-project/sglang); KV reuse: [LMCache](https://github.com/LMCache/LMCache) |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph), [LlamaIndex](https://github.com/run-llama/llama_index), [Haystack](https://github.com/deepset-ai/haystack), [DSPy](https://github.com/stanfordnlp/dspy) |
| Evaluation / tracing | [RAGAS](https://github.com/explodinggradients/ragas), [RAGChecker](https://github.com/amazon-science/RAGChecker), [DeepEval](https://github.com/confident-ai/deepeval), [TruLens](https://github.com/truera/trulens), [Phoenix](https://github.com/Arize-ai/phoenix) |

Rule of thumb: under ~10M chunks, the *database* rarely matters for quality. Chunking, hybrid retrieval and reranking do.

## 17.5 Evaluation loop
1. **Offline:** answer metrics (EM/F1/LLM-judge), retrieval metrics (Recall@k, All@k), groundedness and citation precision. `python -m ragkit run.jsonl` in `code/` computes several at once.
2. **Ablate one component at a time** against the fixed question set.
3. **Online:** log the query, retrieved IDs, prompt, answer, latency and cost; sample and review failures weekly; add failures to the test set.
4. **Attribute each error** to a stage (parse / retrieve / rerank / read). Legal RAG Bench's hierarchical error decomposition is a good model.

## 17.6 Cost and latency levers (in rough order of payoff)
1. Don't retrieve when you don't need to (routing).
2. Retrieve fewer, better passages (rerank) instead of many.
3. Cache: prefix/KV caching for shared prompts; **safe** answer caching with evidence and version checks ([`cache.py`](../code/ragkit/cache.py)).
4. Use a smaller reader for easy queries (RAG-on-a-Diet's idea).
5. For agents, cap and learn search depth (AutoSearch, HiPRAG).

## 17.7 Anti-patterns
- Tuning prompts or RL before measuring retrieval recall.
- Comparing to published numbers instead of your own baseline.
- One giant chunk size for all document types.
- Letting retrieved text act as instructions.
- Shared semantic answer caches without version checks.
