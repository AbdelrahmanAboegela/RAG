# RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

| | |
|---|---|
| **Authors** | Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, Christopher D. Manning (Stanford) |
| **Venue / status** | **ICLR 2024** |
| **Links** | [arXiv:2401.18059](https://arxiv.org/abs/2401.18059) · [code](https://github.com/parthsarthi03/raptor) · toy: [`code/ragkit/raptor.py`](../../code/ragkit/raptor.py) |
| **Section** | 3 and 7, Structured knowledge |

## TL;DR
Build a **tree of summaries** bottom-up: embed chunks, cluster them, summarise each cluster, and repeat on the summaries. At query time, retrieve from **all levels** at once, so a question can match a detail or a theme.

## Method
1. **Leaves:** 100-token chunks embedded with SBERT.
2. **Clustering:** Gaussian Mixture Models over UMAP-reduced embeddings, with the number of clusters chosen by BIC. *Soft* clustering lets a chunk belong to several clusters.
3. **Summaries:** an LLM (GPT-3.5 in the paper) summarises each cluster, and the summaries become the next level's nodes. Repeat until clustering is no longer possible.
4. **Retrieval**, two strategies:
   - *Tree traversal:* top-down, choosing the best children per level.
   - *Collapsed tree:* flatten all nodes and take the top ones up to a token budget. This is the better and simpler strategy.

## Results
Coupled with GPT-4, RAPTOR improved the state of the art on **QuALITY** by about 20% absolute accuracy. It also gained on NarrativeQA and QASPER, the long-document QA sets where thematic questions need synthesis across a document.

## Limitations
- The LLM summarisation cost scales with corpus size.
- Summaries can hallucinate or drop details.
- Clusters are *induced*, so they may not match how the author organised the document. **HiKEY** (ACL 2026) uses the *parsed* hierarchy instead.

## Try it
`python -c "import sys; sys.path.insert(0,'code'); sys.path.insert(0,'code/examples'); from ragkit import RaptorTree; from corpus import DOCS; t=RaptorTree(DOCS); print(t.depth); print(t.search('French cinema', 3))"`
