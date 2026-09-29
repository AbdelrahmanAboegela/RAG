# 16. Domain-specific and enterprise RAG

Most research uses Wikipedia QA. Real deployments are in medicine, law, finance and internal enterprise knowledge, where **retrieval failures masquerade as hallucinations**, documents are long and structured, and correctness has consequences.

## 16.1 Medicine

| Resource | What | Finding |
|---|---|---|
| **MIRAGE + MedRAG** (Xiong et al., Findings ACL 2024; [arXiv:2402.13178](https://arxiv.org/abs/2402.13178); 💻 [MIRAGE](https://github.com/Teddy-XiongGZ/MIRAGE), [MedRAG](https://github.com/Teddy-XiongGZ/MedRAG)) | 7,663 questions from 5 medical QA sets; 41 corpus × retriever × LLM combinations | MedRAG improves six LLMs by up to 18% over CoT, lifting GPT-3.5 and Mixtral to GPT-4 level. **Combining corpora and retrievers is best.** Log-linear scaling and lost-in-the-middle effects also appear in medicine. |
| **UR²** (ACL 2026) | RL with medical corpora + MedQA | 7B: 65.9 average on medical benchmarks ([note](../papers/2026/ur2.md)) |
| **QuCo-RAG** (Findings 2026) | corpus-statistics triggers validated on biomedical QA | [note](../papers/2026/quco-rag.md) |
| **ParallaxRAG** (ACL 2026) | KG-RAG with strong biomedical generalisation | [note](../papers/2026/parallaxrag.md) |

## 16.2 Law

**Legal RAG Bench** ([arXiv:2603.01710](https://arxiv.org/abs/2603.01710), 2026): 4,876 passages from the Victorian Criminal Charge Book and 100 expert questions, in a **full-factorial design** over embedders and LLMs.
- **Retrieval is the primary driver** of legal RAG quality. The best embedder added +17.5 correctness, +4.5 groundedness and +34 retrieval accuracy.
- **Many "hallucinations" were retrieval failures.**

This matches The Retrieval Bottleneck (ACL 2026) and BrowseComp-Plus in very different settings.

## 16.3 Finance

- **FinanceBench** (Patronus AI; [arXiv:2311.11944](https://arxiv.org/abs/2311.11944); 💻 [patronus-ai/financebench](https://github.com/patronus-ai/financebench)): about 10K QA pairs over SEC filings, with a 150-case open sample. In 2023, GPT-4-Turbo with a retrieval system answered incorrectly or refused **81%** of sampled questions.
- **AgenticRAG** (2026, [arXiv:2605.05538](https://arxiv.org/abs/2605.05538)): giving a reasoning LLM **search / find / open / summarize** tools over existing enterprise search reached **92%** answer correctness on FinanceBench, within 2 points of oracle evidence. Moving from single-shot retrieval to agentic tool use was the largest factor (5.9×).
- **FinCacheServe** (2026): answer caching over *changing* filings, keyed by document versions and evidence fingerprints (see [10](10-efficiency.md)).

## 16.4 Enterprise knowledge bases

What makes enterprise RAG different:
1. **Permissions:** retrieval must respect per-user access control lists. Filter at the index, never rely on the prompt.
2. **Heterogeneous formats:** PDFs, slides, spreadsheets, tickets, wikis, email. Parsing quality dominates (see HiKEY and [17](17-production-guide.md)).
3. **Mutable documents:** versioning, freshness and cache invalidation.
4. **Existing search stacks:** the AgenticRAG result suggests you can *layer an agent on top of* existing enterprise search instead of replacing it.
5. **Evaluation data is scarce:** build a small, expert-labelled test set early; 100 good questions go a long way, as Legal RAG Bench shows.

## 16.5 Multimodal and wearable assistants

**CRAG-MM** (Meta; KDD 2026 proceedings; [arXiv:2510.26160](https://arxiv.org/abs/2510.26160)): 6.5K (image, question, answer) triplets and 2K multi-turn conversations across 13 domains, including 6.2K **egocentric images** mimicking wearable devices. It was the basis of KDD Cup 2025 (about 1K participants, 5K submissions). Straightforward RAG achieves only **32% / 43%** truthfulness (single- / multi-turn), and industry solutions score similarly (32% / 45%). See also EgoMemory ([note](../papers/2026/egomemory.md)).

## 16.6 Takeaways
- In every domain benchmark above, **retrieval quality is the main lever**.
- Domain corpora + general corpora + multiple retrievers beat any single source (MIRAGE).
- Agentic tool use over existing search is a strong, cheap upgrade path (AgenticRAG).
- Build expert test sets and report *groundedness* separately from *correctness* (Legal RAG Bench; FRANQ).
