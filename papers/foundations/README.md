# Foundations and the classic "advanced RAG" toolkit (2017–2024)

These are the papers every later paper assumes you know. Each entry covers **what** the paper did, **how** it did it, and **why it matters now**. Detailed discussion is in [docs/01](../../docs/01-foundations.md), [docs/02](../../docs/02-failure-modes.md) and [docs/03](../../docs/03-classic-advanced-rag.md).

Legend: 📄 paper · 💻 official code

---

## A. Retrieval-augmented language models

### RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., NeurIPS 2020)
📄 [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- **What:** coined "RAG". A DPR retriever is combined with a BART generator, trained end-to-end on QA, fact verification and generation.
- **How:** retrieved passages are latent variables. *RAG-Sequence* marginalises over documents per output sequence; *RAG-Token* marginalises per token. The query encoder and generator are fine-tuned, and the document index is frozen.
- **Why now:** it established the retrieve-then-read split that the 2025–26 agentic work is dissolving.

### REALM (Guu et al., ICML 2020)
📄 [arXiv:2002.08909](https://arxiv.org/abs/2002.08909)
- **What:** retrieval during *pre-training*: masked-LM training with a learned retriever over Wikipedia.
- **How:** backpropagates through top-k retrieval and refreshes the index asynchronously.
- **Why now:** it is the ancestor of "retrieval is part of the model", a line that LatentRAG's jointly trained retriever continues.

### FiD: Fusion-in-Decoder (Izacard & Grave, EACL 2021)
📄 [arXiv:2007.01282](https://arxiv.org/abs/2007.01282)
- **What / how:** encodes each passage separately and fuses them all in the decoder's cross-attention.
- **Why now:** it showed that reading *many* passages beats reading a few well-chosen ones. That intuition is now challenged by lost-in-the-middle and context-noise results.

### RETRO (Borgeaud et al., ICML 2022)
📄 [arXiv:2112.04426](https://arxiv.org/abs/2112.04426)
- **What:** a 7.5B model with chunked cross-attention to a 2-trillion-token retrieval database matched GPT-3 (175B) on the Pile.
- **Why now:** it is the strongest evidence that retrieval can substitute for parameters.

### Atlas (Izacard et al., JMLR 2023)
📄 [arXiv:2208.03299](https://arxiv.org/abs/2208.03299) · 💻 [facebookresearch/atlas](https://github.com/facebookresearch/atlas)
- **What:** a jointly pre-trained retriever and reader. With 11B parameters it beat a 540B PaLM on few-shot NaturalQuestions with 64 examples.

---

## B. Retrievers

### BM25 (Robertson & Zaragoza, 2009)
- **What:** term-frequency saturation and length normalisation over inverted indexes.
- **Why now:** still a strong baseline. QuCo-RAG and HiKEY use it, and hybrid BM25 + dense is the production default. See [`code/ragkit/bm25.py`](../../code/ragkit/bm25.py).

### DPR: Dense Passage Retrieval (Karpukhin et al., EMNLP 2020)
📄 [arXiv:2004.04906](https://arxiv.org/abs/2004.04906) · 💻 [facebookresearch/DPR](https://github.com/facebookresearch/DPR)
- **What / how:** a BERT bi-encoder trained contrastively with in-batch negatives and BM25 hard negatives. It also produced the **21M × 100-word Wikipedia passage** corpus that most QA-RAG papers still use.

### ColBERT (Khattab & Zaharia, SIGIR 2020)
📄 [arXiv:2004.12832](https://arxiv.org/abs/2004.12832) · 💻 [stanford-futuredata/ColBERT](https://github.com/stanford-futuredata/ColBERT)
- **What / how:** *late interaction*: one vector per token, scored by the sum of per-query-token MaxSim.
- **Why now:** ColPali brings the same idea to page images, and HiKEY uses MaxSim to aggregate units to sections.

### SPLADE (Formal et al., SIGIR 2021)
📄 [arXiv:2107.05720](https://arxiv.org/abs/2107.05720) · 💻 [naver/splade](https://github.com/naver/splade)
- **What:** learned *sparse* expansion. It keeps inverted-index efficiency while adding semantic matching.

### Contriever (Izacard et al., TMLR 2022)
📄 [arXiv:2112.09118](https://arxiv.org/abs/2112.09118) · 💻 [facebookresearch/contriever](https://github.com/facebookresearch/contriever)
- **What:** an unsupervised contrastive dense retriever. It showed dense retrieval can beat BM25 zero-shot.

### E5, BGE, and LLM-based embedders (2022–2025)
📄 E5 [arXiv:2212.03533](https://arxiv.org/abs/2212.03533) · 💻 BGE [FlagOpen/FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)
- **What:** general-purpose embedders trained on weakly supervised pairs, then fine-tuned. E5-base-v2 is the Search-R1 default. The 2026 papers use Qwen3-Embedding, NV-Embed-v2 and gte-Qwen2.

### HyDE: Hypothetical Document Embeddings (Gao et al., ACL 2023)
📄 [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- **What / how:** generate a *fake* answer document with an LLM, embed it, and retrieve real documents near it.
- **Why now:** it is the simplest fix for the query–document gap, the gap QueryLink tackles for memories.

### Query Rewriting for RAG (Ma et al., EMNLP 2023)
📄 [arXiv:2305.14283](https://arxiv.org/abs/2305.14283)
- **What:** a small rewriter trained with RL, using the reader's answer quality as reward. It is an early instance of "RL on the retrieval interface".

---

## C. Why vanilla RAG fails (evidence papers)

### Lost in the Middle (Liu et al., TACL 2024)
📄 [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) · 💻 [nelson-liu/lost-in-the-middle](https://github.com/nelson-liu/lost-in-the-middle)
- **What:** accuracy follows a **U-curve** over the position of the relevant document in the context. Models use the beginning and end best.
- **Why now:** it motivates rerank-then-truncate, memory curation (State-Aware RAG) and evidence packing (HiKEY).

### Making Retrieval-Augmented LMs Robust to Irrelevant Context (Yoran et al., ICLR 2024)
📄 [arXiv:2310.01558](https://arxiv.org/abs/2310.01558)
- **What:** irrelevant retrieved passages *reduce* accuracy below no-retrieval. NLI filtering and fine-tuning on mixed contexts are proposed as mitigations.

### Knowledge Conflicts for LLMs: A Survey (Xu et al., EMNLP 2024)
📄 [arXiv:2403.08319](https://arxiv.org/abs/2403.08319)
- **What:** a taxonomy of context–memory, inter-context and intra-memory conflicts.

### ClashEval (Wu, Wu & Zou, NeurIPS 2024 D&B)
📄 [arXiv:2404.10198](https://arxiv.org/abs/2404.10198)
- **What:** perturb retrieved facts by increasing amounts and measure when models adopt the wrong context. Models over-trust context even when their prior knowledge is right.

### PoisonedRAG (Zou et al., USENIX Security 2025)
📄 [arXiv:2402.07867](https://arxiv.org/abs/2402.07867) · 💻 [sleeepeer/PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG)
- **What:** injecting about 5 crafted texts per target question into a million-document corpus achieves a ~90% attack success rate.

---

## D. The pre-RL "advanced RAG" toolkit

### Self-Ask (Press et al., Findings EMNLP 2023)
📄 [arXiv:2210.03350](https://arxiv.org/abs/2210.03350)
- **What:** the model asks itself follow-up questions, answered by search. It introduced **Bamboogle** and the "compositionality gap".

### IRCoT (Trivedi et al., ACL 2023)
📄 [arXiv:2212.10509](https://arxiv.org/abs/2212.10509) · 💻 [StonyBrookNLP/ircot](https://github.com/StonyBrookNLP/ircot)
- **What / how:** interleave retrieval with chain-of-thought. Each new CoT sentence becomes the next query.
- **Why now:** the standard iterative baseline (T²RAG, RAG-on-a-Diet and SPARKLE compare against it).

### FLARE: Active Retrieval Augmented Generation (Jiang et al., EMNLP 2023)
📄 [arXiv:2305.06983](https://arxiv.org/abs/2305.06983) · 💻 [jzbjyb/FLARE](https://github.com/jzbjyb/FLARE)
- **What / how:** generate a tentative next sentence. If any token has low probability, retrieve using that sentence as the query, then regenerate.
- **Why now:** the archetype of *model-internal* retrieval triggers, which QuCo-RAG argues are unreliable.

### DRAGIN (Su et al., ACL 2024)
📄 [arXiv:2403.10081](https://arxiv.org/abs/2403.10081) · 💻 [oneal2000/DRAGIN](https://github.com/oneal2000/DRAGIN)
- **What:** triggers on token uncertainty × attention-based importance, and builds the query from attention over the context. It is a QuCo-RAG baseline.

### Self-RAG (Asai et al., ICLR 2024)
📄 [arXiv:2310.11511](https://arxiv.org/abs/2310.11511) · 💻 [AkariAsai/self-rag](https://github.com/AkariAsai/self-rag)
- **What / how:** fine-tune the LM to emit **reflection tokens**: `[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`. At inference, these gate retrieval and rank candidate segments. The labels are distilled from GPT-4.
- **Why now:** the first model that *learned* when to retrieve, with supervised labels. Search-R1 replaced the labels with RL.

### CRAG: Corrective RAG (Yan et al., 2024)
📄 [arXiv:2401.15884](https://arxiv.org/abs/2401.15884) · 💻 [HuskyInSalt/CRAG](https://github.com/HuskyInSalt/CRAG)
- **What:** a light evaluator grades retrieval as Correct, Incorrect or Ambiguous. It falls back to web search and applies decompose-then-recompose filtering.
- ⚠ Not to be confused with the **CRAG benchmark** (Meta, 2024) in [docs/11](../../docs/11-evaluation.md).

### Adaptive-RAG (Jeong et al., NAACL 2024)
📄 [arXiv:2403.14403](https://arxiv.org/abs/2403.14403) · 💻 [starsuzi/Adaptive-RAG](https://github.com/starsuzi/Adaptive-RAG)
- **What:** a small classifier predicts query complexity and routes to no retrieval, single-step or multi-step retrieval. It is the ancestor of UR²'s difficulty curriculum and a RAG-on-a-Diet baseline.

### RAPTOR (Sarthi et al., ICLR 2024)
📄 [arXiv:2401.18059](https://arxiv.org/abs/2401.18059) · 💻 [parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)
- **What / how:** recursively cluster chunks (GMM over embeddings), summarise each cluster, and repeat to build a tree. Retrieval happens across all levels.
- **Why now:** an *induced* hierarchy, the counterpart of HiKEY's *parsed* hierarchy.

### GraphRAG: From Local to Global (Edge et al., Microsoft, 2024)
📄 [arXiv:2404.16130](https://arxiv.org/abs/2404.16130) · 💻 [microsoft/graphrag](https://github.com/microsoft/graphrag)
- **What / how:** an LLM extracts an entity–relation graph, Leiden clustering finds communities, and the LLM writes community summaries. **Global** questions ("What are the main themes?") are answered map-reduce style over the summaries.
- **Why now:** it opened the graph-RAG line. Its indexing cost is what T²RAG and LightRAG react to.

### HippoRAG (Gutiérrez et al., NeurIPS 2024) and HippoRAG 2 (ICML 2025)
📄 [arXiv:2405.14831](https://arxiv.org/abs/2405.14831) · [arXiv:2502.14802](https://arxiv.org/abs/2502.14802) · 💻 [OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG)
- **What / how:** inspired by hippocampal indexing theory. OpenIE builds a knowledge graph, query entities seed **Personalized PageRank**, and PPR scores rank passages. Version 2 adds passage nodes and query-to-triple matching.
- **Why now:** it is State-Aware RAG's strongest memory baseline and T²RAG's `hippo` baseline, and PPR reappears in HiGoE.

### LightRAG (Guo et al., 2024)
📄 [arXiv:2410.05779](https://arxiv.org/abs/2410.05779) · 💻 [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)
- **What:** dual-level (entity and theme) graph retrieval with incremental updates, much cheaper than GraphRAG. It is widely used in practice.

### RECOMP (Xu et al., ICLR 2024) and LongLLMLingua (Jiang et al., ACL 2024)
📄 [arXiv:2310.04408](https://arxiv.org/abs/2310.04408) · [arXiv:2310.06839](https://arxiv.org/abs/2310.06839)
- **What:** compress retrieved context (extractive or abstractive summaries; token-level pruning) before reading. They are the "one-time compression" that State-Aware RAG argues is insufficient for multi-hop.

### Chain-of-Note (Yu et al., EMNLP 2024)
📄 [arXiv:2311.09210](https://arxiv.org/abs/2311.09210)
- **What:** the model writes a reading note per retrieved document before answering, which improves robustness to noisy retrieval.

### Speculative RAG (Wang et al., ICLR 2025)
📄 [arXiv:2407.08223](https://arxiv.org/abs/2407.08223)
- **What:** a small specialist drafts answers from document subsets in parallel, and a large generalist verifies them.

### RankRAG (Yu et al., NeurIPS 2024)
📄 [arXiv:2407.02485](https://arxiv.org/abs/2407.02485)
- **What:** instruction-tunes a single LLM to both rerank contexts and generate answers.

### Long-context LLMs meet RAG (Jin et al., ICLR 2025)
📄 [arXiv:2410.05983](https://arxiv.org/abs/2410.05983)
- **What:** with long-context models, adding more retrieved passages first helps and then *hurts*, because hard negatives distract. It proposes retrieval reordering and RAG-specific tuning.

---

## E. Surveys to cite

| Survey | Link |
|---|---|
| Gao et al., *Retrieval-Augmented Generation for Large Language Models: A Survey* (2023/24) | [arXiv:2312.10997](https://arxiv.org/abs/2312.10997) · 💻 [Tongji-KGLLM/RAG-Survey](https://github.com/Tongji-KGLLM/RAG-Survey) |
| Li et al., *Towards Agentic RAG with Deep Reasoning: A Survey of RAG-Reasoning Systems in LLMs* (2025) | [arXiv:2507.09477](https://arxiv.org/abs/2507.09477) · 💻 [DavidZWZ/Awesome-RAG-Reasoning](https://github.com/DavidZWZ/Awesome-RAG-Reasoning) |
| Singh et al., *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG* (2025) | [arXiv:2501.09136](https://arxiv.org/abs/2501.09136) |
| Mishra et al., *SoK: Agentic RAG: Taxonomy, Architectures, Evaluation, and Research Directions* (March 2026) | [arXiv:2603.07379](https://arxiv.org/abs/2603.07379) |
| Dong et al., *From RAG to Agentic Deep Research* (KDD 2026 tutorial paper) | [PDF](https://tutorial.lunadong.com/paper.pdf) · [paper DB](https://papers.lunadong.com) |
| Gao et al., *Scaling Beyond Context: A Survey of Multimodal RAG for Document Understanding* (ACL 2026) | [ACL Anthology](https://aclanthology.org/2026.acl-long.204/) |
| *A Comprehensive Survey on RL-based Agentic Search* | 💻 [ventr1c/Awesome-RL-based-Agentic-Search-Papers](https://github.com/ventr1c/Awesome-RL-based-Agentic-Search-Papers) |
| Graph RAG resources | 💻 [DEEP-PolyU/Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) |
