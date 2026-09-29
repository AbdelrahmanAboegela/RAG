# BrowseComp-Plus: A More Fair and Transparent Evaluation Benchmark of Deep-Research Agent

| | |
|---|---|
| **Authors** | Zijian Chen, Xueguang Ma, Shengyao Zhuang, Ping Nie, Kai Zou, Andrew Liu, et al. |
| **Venue / status** | **ACL 2026 main** (per the official repo); arXiv August 2025 |
| **Links** | [arXiv:2508.06600](https://arxiv.org/abs/2508.06600) · [code](https://github.com/texttron/BrowseComp-Plus) · HF `Tevatron/browsecomp-plus`, `Tevatron/browsecomp-plus-corpus` |
| **Section** | 11, Evaluation / 13, Deep research |
| **Verified** | arXiv abstract and repo README (September 2026) |

## TL;DR
BrowseComp-Plus is OpenAI's BrowseComp rebuilt on a **fixed, curated corpus** of about 100K human-verified documents, instead of the live web. It has 830 queries. Because the corpus is fixed, you can swap the **retriever** while holding the **agent** constant, and the reverse, which you cannot do against a black-box web search API.

## Why it matters
- **Reproducibility:** live-web benchmarks change daily and depend on opaque search APIs.
- **Attribution:** with a fixed corpus, gains can be attributed to the retriever or to the LLM.
- **Headline finding (abstract):** Search-R1 with BM25 reaches **3.86%** accuracy, GPT-5 reaches **55.9%**, and GPT-5 with the **Qwen3-Embedding-8B** retriever reaches **70.1% with fewer search calls**. A better retriever made the frontier model both *more accurate* and *more efficient*. This is a third independent data point for [The Retrieval Bottleneck](retrieval-bottleneck.md), alongside State-Aware RAG (+22.2% from Google Search) and Legal RAG Bench.

## How to use it
```bash
# agent evaluation (from the repo README)
python scripts_evaluation/evaluate_run.py --input_dir runs/my_model
# retrieval-only evaluation (TREC format)
python -m pyserini.eval.trec_eval -c -m recall.5,100,1000 -m ndcg_cut.10 topics-qrels/qrel_evidence.txt {YOUR_TREC_RUN_FILE}
```

## Used by
OpenResearcher (2026) trains on an offline corpus and reports 54.8% on BrowseComp-Plus for a 30B-A3B model.

## Discussion
The 2025 RL-search recipe (Search-R1 + BM25 over Wikipedia) scores under 4% here. What does that say about the seven-QA-set benchmark suite those papers report on?
