# 1. Foundations: the RAG pipeline and its components

> **Code:** [`code/ragkit/`](../code/ragkit/) implements BM25, a toy dense retriever, RRF fusion and chunking. Run `python code/examples/01_hybrid_retrieval.py`.

## 1.1 The pipeline

```
          offline                                          online
documents ─► parse ─► chunk ─► embed/index      query ─► (rewrite) ─► retrieve ─► rerank ─► (compress) ─► generate ─► answer + citations
```

Every box is a decision that changes results more than most model upgrades.

## 1.2 Parsing and chunking

**Parsing** turns PDFs, HTML and slides into text and structure. It is the unglamorous stage where most production errors start. Tables, figures, headers and reading order are routinely lost. HiKEY's result (+12.9% recall from exploiting document hierarchy) is mostly a parsing result.

**Chunking** fixes the retrievable unit:

| Strategy | Idea | Trade-off |
|---|---|---|
| Fixed windows | N words/tokens with overlap. DPR and the QA-RAG literature use **100-word** passages | simple and reproducible; splits facts |
| Sentence / paragraph packing | never split a sentence; pack up to N | better coherence; variable size |
| Structure-aware | split on headings, sections, list items | needs good parsing; see HiKEY |
| Semantic | split where embedding similarity between neighbours drops | expensive; fragile thresholds |
| Propositions / triplets | atomic facts as units (Dense X Retrieval, T²RAG) | precise; loses context unless you keep the source chunk |
| Late chunking | embed the whole document with a long-context encoder, then pool per chunk ([Jina, arXiv:2409.04701](https://arxiv.org/abs/2409.04701)) | chunks keep document context |
| Contextual retrieval | prepend an LLM-written sentence that situates each chunk in its document before embedding (Anthropic, 2024) | large recall gains; indexing cost |

**Rule of thumb:** smaller units give higher precision and need more hops. Larger units give higher recall and more noise.

## 1.3 Retrieval

### Sparse
**BM25** scores term overlap with TF saturation (k1) and length normalisation (b). It needs no training, works well out of domain and handles rare entities exactly. That last point matters because rare entities are where LLMs hallucinate (QuCo-RAG). **SPLADE** learns sparse term expansions.

### Dense
**Bi-encoders** (DPR, Contriever, E5, BGE, GTE, Qwen3-Embedding, NV-Embed-v2) embed the query and document separately and score them by dot product or cosine. At scale they are served by an ANN index (FAISS flat, HNSW, IVF-PQ).
- They are trained contrastively with in-batch and hard negatives.
- Most need **instruction or prefix conventions** (`query: ` / `passage: ` for E5). Forgetting these silently costs several points.
- Compare them on [MTEB](https://arxiv.org/abs/2210.07316) and [BEIR](https://arxiv.org/abs/2104.08663). For reasoning-heavy queries, use [BRIGHT](https://arxiv.org/abs/2407.12883), where standard embedders do poorly.

### Late interaction
**ColBERT** keeps one vector per token and scores with the sum of per-query-token MaxSim. It is more accurate than a single vector, with a bigger index. ColPali applies the same idea to page images (Section 9).

### Hybrid and fusion
Run BM25 and a dense retriever in parallel and fuse with **Reciprocal Rank Fusion**: `score(d) = Σ 1/(k + rank(d))`, with k = 60. RRF needs no score calibration. Hybrid is the default in production, and HiKEY's document router is hybrid.

## 1.4 Query-side techniques

- **Rewriting:** ask the LLM (or a small RL-trained rewriter; Ma et al., 2023) to rewrite the query for the retriever.
- **HyDE:** generate a hypothetical answer and retrieve with *its* embedding.
- **Decomposition:** split multi-hop questions into sub-questions (Self-Ask, least-to-most). T²RAG's placeholder triplets are a structured version.
- **Multi-query / RAG-Fusion:** several paraphrases, fused with RRF.

## 1.5 Reranking

Retrieve 50–100 candidates cheaply, then rerank with a **cross-encoder** (query and document jointly encoded, e.g. BGE-reranker, monoT5) or an **LLM reranker** (listwise, e.g. RankGPT; RankRAG trains a single model to rerank and generate). Reranking is usually the cheapest large accuracy gain in a pipeline.

## 1.6 Generation

- **Prompting:** instruct the model to answer only from context and to cite passage IDs. Put the most relevant passages first *and* last (see lost-in-the-middle, Section 2).
- **Fine-tuning for RAG:** RA-DIT, InstructRAG, RankRAG, and Self-RAG (reflection tokens) train the reader to use, and to ignore, retrieved context.
- **Citations and attribution:** [ALCE](https://arxiv.org/abs/2305.14627) (💻 [princeton-nlp/ALCE](https://github.com/princeton-nlp/ALCE)) benchmarks citation quality.

## 1.7 Frameworks and toolkits

| Purpose | Tools |
|---|---|
| Research RAG toolkit (datasets, 20+ methods, one format) | [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG), [UltraRAG](https://github.com/OpenBMB/UltraRAG) |
| Application frameworks | [LlamaIndex](https://github.com/run-llama/llama_index), [LangGraph](https://github.com/langchain-ai/langgraph), [Haystack](https://github.com/deepset-ai/haystack), [RAGFlow](https://github.com/infiniflow/ragflow) |
| Graph RAG | [microsoft/graphrag](https://github.com/microsoft/graphrag), [LightRAG](https://github.com/HKUDS/LightRAG), [nano-graphrag](https://github.com/gusye1234/nano-graphrag), [HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) |
| Embeddings and rerankers | [FlagEmbedding (BGE)](https://github.com/FlagOpen/FlagEmbedding), [ColBERT](https://github.com/stanford-futuredata/ColBERT), [SPLADE](https://github.com/naver/splade) |
| RL for search agents | [verl](https://github.com/volcengine/verl), [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF), [Search-R1](https://github.com/PeterGriffinJin/Search-R1) |
| Serving and caching | [vLLM](https://github.com/vllm-project/vllm), [LMCache](https://github.com/LMCache/LMCache) |
| Evaluation | [RAGAS](https://github.com/explodinggradients/ragas), [ARES](https://github.com/stanford-futuredata/ARES) |

## Check your understanding
1. Why does BM25 often beat dense retrievers on queries about rare named entities?
2. You switch from 100-word to 400-word chunks. Predict what happens to recall@5, answer accuracy and latency.
3. Why can RRF fuse BM25 scores (unbounded) with cosine similarities (between −1 and 1) without normalisation?
