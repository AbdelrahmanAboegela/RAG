# 9. Multimodal RAG

Real documents are charts, tables, scans, slides and videos. Text-only pipelines lose that information at parsing time.

## 9.1 Two retrieval paradigms

| Paradigm | How | Examples | Trade-off |
|---|---|---|---|
| **Parse then embed text** | OCR/layout → text chunks (+ captions for figures) | classic pipelines; NV-Ingest | cheap to read; loses visual content |
| **Embed the page image** | a VLM encodes page screenshots; late interaction over patches | **ColPali / ColQwen** ([arXiv:2407.01449](https://arxiv.org/abs/2407.01449), 💻 [illuin-tech/colpali](https://github.com/illuin-tech/colpali)); **VisRAG** ([arXiv:2410.10594](https://arxiv.org/abs/2410.10594), 💻 [openbmb/VisRAG](https://github.com/openbmb/VisRAG)); M3DocRAG | keeps layout and charts; token-heavy reading |
| **Hierarchical multimodal** (2026) | parse structure, keep typed units (text, table, figure) with visual + text embeddings | **HiKEY** ([note](../papers/2026/hikey.md)) | best of both; complex pipeline |

**Survey:** *Scaling Beyond Context: A Survey of Multimodal RAG for Document Understanding* (ACL 2026 main, [Anthology](https://aclanthology.org/2026.acl-long.204/)). It gives a taxonomy by domain, retrieval modality and granularity, covers graph and agentic multimodal RAG, and lists open challenges in efficiency, fine-grained representation and robustness.

## 9.2 Charts are hard: Chart-MRAG (ACL 2026 main)

Note: [papers/2026/chart-mrag.md](../papers/2026/chart-mrag.md)
- It is a benchmark of 4,738 chart-grounded QA pairs across 8 domains, built with the CHARGE pipeline.
- **Retrieval:** unified multimodal embedders struggle on charts.
- **Reading:** even with *ground-truth* retrieval, the best MLLMs reach only **71.15% Correctness / 80.74% Coverage** (camera-ready; the repo README's older 58.19% / 73.87% should not be quoted).
- **Bias:** models prefer text over visual evidence.

## 9.3 When modalities disagree: CMC-Bench (workshop, 2026)

Note: [papers/2026/cmc-bench.md](../papers/2026/cmc-bench.md). It tests conflicting image and text evidence: models abstain or fabricate. Pair it with Chart-MRAG's text-over-visual bias. Together they suggest MLLMs do not yet *weigh* modalities; they default to one.

## 9.4 Video and personal memory
**EgoMemory** (Findings ACL 2026, [note](../papers/2026/egomemory.md)): personalised retrieval over long egocentric video with a training-free MLLM + reflective-CoT retriever.

## 9.5 More multimodal systems and benchmarks

| Work | Status | Idea |
|---|---|---|
| **M3DocRAG** (2024) | arXiv | ColPali retrieval + Qwen2-VL reading over 3,000+ PDFs / 40,000+ pages; introduced **M3DocVQA** ([arXiv:2411.04952](https://arxiv.org/abs/2411.04952)) |
| **VDocRAG** (CVPR 2025) | CVPR | unified image format for mixed documents; self-supervised retrieval pre-training; **OpenDocVQA** ([arXiv:2504.09795](https://arxiv.org/abs/2504.09795)) |
| **MegaRAG** | ACL 2026 main | multimodal knowledge graphs ([note](../papers/2026/megarag.md)) |
| **MG²-RAG** | arXiv 2026 | multi-granularity multimodal graph fusing text entities and visual regions |
| **Chain of Evidence** | arXiv 2026 | pixel-level **bounding-box attribution** over screenshots for iterative RAG |
| **SimpleSearch-VL** | arXiv 2026 | multimodal agentic deep search from 5K SFT + 2K RL examples |
| **CRAG-MM** | KDD 2026 | egocentric-image, multi-turn RAG benchmark; plain RAG reaches 32% / 43% truthfulness ([arXiv:2510.26160](https://arxiv.org/abs/2510.26160)) |
| **MMDeepResearch-Bench**, **MiroEval** | arXiv 2026 | multimodal *deep research* evaluation ([13](13-deep-research.md)) |

## 9.6 Open problems
- Fine-grained **chart and table reasoning** after retrieval: the reader is the bottleneck, not the retriever (compare HiKEY: recall +12.9%, QA only +6.8%).
- **Modality arbitration:** deciding which evidence to trust when text and image disagree.
- **Cost:** page images take thousands of tokens each; token-budgeted packing (HiKEY) is one answer.
