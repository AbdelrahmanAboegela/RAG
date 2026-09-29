# HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering

| | |
|---|---|
| **Authors** | Joongmin Shin, Gyuho Shim, Jeongbae Park, Jaehyung Seo, Heuiseok Lim |
| **Venue / status** | **ACL 2026 main** (per the arXiv comment). arXiv May 28, 2026 |
| **Links** | [arXiv:2605.29606](https://arxiv.org/abs/2605.29606) · code: not linked as of September 2026 |
| **Section** | 7, Knowledge representation (also relevant to 9, Multimodal) |
| **Verified** | Method and numbers from arXiv HTML v1 (September 2026) |

## TL;DR
HiKEY treats a document's **section hierarchy** as a first-class retrieval signal. It routes from document to section to unit, and packs evidence with its governing headers under a token budget. It reports up to +12.9% retrieval recall and +6.8% end-to-end QA on multi-page, multimodal PDFs.

## 1. Problem and gap
In industrial document QA over thousands of PDFs, two things break:
- **Routing:** flat chunk retrieval misses the right *document*.
- **Evidence fragmentation:** the answer is spread across a table, a figure and a paragraph on different pages.

Page-image retrieval (ColPali, M3DocRAG, VDocRAG) is token-hungry and noisy. Text chunking throws away layout and hierarchy.

## 2. Key idea
Documents already have a tree (Title › Section 5 › 5.3 › Table 2). Parse it, index it, and **retrieve coarse-to-fine along it**.

## 3. Method
1. **Document Hierarchical Parsing (DHP):** an LVLM-based parser (M3DocDep) turns each PDF into a heterogeneous graph. Blocks (text, table, figure) are nodes, and tree edges encode parent–child relations. Each node gets its ancestor path. Two indexes are built: **Doc cards** (title plus all section paths) for routing, and **Sec cards** (section-level multimodal units) for ranking. Tables and figures without captions borrow the preceding text as "upper context".
2. **Coarse-to-fine retrieval:**
   - *Stage 1, document routing:* hybrid BM25 + dense (gte-Qwen2-7B-instruct) over Doc cards narrows thousands of documents to dozens.
   - *Stage 2, section ranking:* text units use hybrid fusion; tables and images use visual embeddings (MM-Embed) fused with upper-context text. Unit scores are aggregated to sections by MaxSim and blended with the document score.
3. **Token-efficient evidence assembly:** each selected section contributes its best unit plus its *governing headers*. Under the budget, the rest is filled first with **sibling units** (same parent section) and then **semantic associates** (similar units elsewhere).
4. **Reader:** Qwen2.5-VL-7B-Instruct with a 16K budget, the same for all methods.

## 4. Results
- **Benchmarks:** M3DocVQA, and FRAMES re-rendered as multi-page PDFs.
- **Baselines:** chunkers (LumberChunker, Meta-Chunker, MultiDocFusion), graph-text RAG (RAPTOR, HopRAG), page-level multimodal (M3DocRAG, VDocRAG), and multimodal graph methods (MoLoRAG, SimpleDoc).
- **FRAMES document retrieval:** recall 73.3 (+7.1); **"All" (every gold document retrieved) 46.2 (+11.4)**, the key multi-hop gain.
- **M3DocVQA:** recall 84.9 (+1.9), All 73.6 (+3.1). **End-to-end EM:** 27.5 on M3DocVQA (+1.9), 10.5 on FRAMES (+2.7).
- It wins at small budgets (0.5K–2K tokens); competitors catch up at large budgets.
- **Ablation:** doc→section routing reaches 88.6 average R@10, against 87.7 for doc-only and 76.1 for section-only.

## 5. Limitations
- **(stated)** Offline parsing is costly.
- **(stated)** Parsing and OCR errors propagate into wrong section paths.
- **(stated)** It helps little on weakly structured documents (receipts, slides).
- **(stated)** Recall rises 12.9% but QA only 6.8%, so the reader, not retrieval, becomes the bottleneck.

## 6. What changed vs. the previous approach
It moves from "chunks or pages" to **"the document's own tree"** as the index structure, and it makes token budget an explicit design constraint.

## 7. Discussion questions
1. Compare HiKEY's hierarchy with RAPTOR's. One is *parsed* from the author's structure, the other *induced* by clustering. When would each win?
2. Why does the "All" metric matter more than recall for multi-hop document QA?
