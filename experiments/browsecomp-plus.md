# Evaluating on BrowseComp-Plus

**Repo:** [texttron/BrowseComp-Plus](https://github.com/texttron/BrowseComp-Plus) · **Paper:** [arXiv:2508.06600](https://arxiv.org/abs/2508.06600) (ACL 2026 main per the repo) · **Data:** HF `Tevatron/browsecomp-plus` (queries, with answers and evidence) and `Tevatron/browsecomp-plus-corpus` (~100K documents) · **Notes:** [papers/2026/browsecomp-plus.md](../papers/2026/browsecomp-plus.md)

Use it when you want to measure a **deep-research agent** or a **retriever** under a fixed, reproducible corpus.

## Evaluate an agent run (from the repo README)
```bash
python scripts_evaluation/evaluate_run.py --input_dir runs/my_model
```

## Evaluate a retriever alone (TREC run file)
```bash
python -m pyserini.eval.trec_eval -c -m recall.5,100,1000 -m ndcg_cut.10 \
    topics-qrels/qrel_evidence.txt {YOUR_TREC_RUN_FILE}
```

## Experiments worth running
1. **Same agent, different retrievers** (BM25 vs a dense embedder). The paper reports that GPT-5 goes from 55.9% (BM25) to 70.1% (Qwen3-Embedding-8B) *with fewer search calls*.
2. **Same retriever, different agents**, including a Search-R1-style small model (3.86% with BM25 in the paper), to see how far short-QA RL recipes transfer.
3. Log the **number of search calls** and **citation accuracy** alongside accuracy.

Check the repo README for current run-file formats and leaderboard submission instructions; they may have changed since September 2026.
