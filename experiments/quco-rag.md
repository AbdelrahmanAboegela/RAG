# Reproducing QuCo-RAG

**Repo:** [ZhishanQ/QuCo-RAG](https://github.com/ZhishanQ/QuCo-RAG) · **Paper:** [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) (Findings ACL 2026) · **Notes:** [papers/2026/quco-rag.md](../papers/2026/quco-rag.md)

QuCo-RAG needs **no training** and is the cheapest 2026 method to reproduce. You need GPU inference for OLMo-2 (7B, 13B or 32B), an Elasticsearch BM25 index over Wikipedia, and network access to the Infini-gram API.

## Setup and run (from the repo README)

```bash
git clone https://github.com/ZhishanQ/QuCo-RAG.git
cd QuCo-RAG
conda create -n quco-rag python=3.9 && conda activate quco-rag
pip install -r requirements.txt

cd src
python main_quco.py -c ../config/OLMo-2-1124-7B-Instruct/2WikiMultihopQA/QuCo-RAG.json

python evaluate.py --dir ../result/QuCo-RAG_OLMo-2-1124-7B-Instruct_2wikimultihopqa/1
```

The repo ships pre-built Elasticsearch indices and optional cache files that speed up experiments 2–5×. Use them: Infini-gram calls are fast (milliseconds), but thousands of them across 1,000 questions × several configurations add up.

## Key hyperparameters (from the paper)

| Parameter | Value |
|---|---|
| Entity frequency threshold τ_entity | 10³ (results stable from 10³ to 10⁷) |
| Co-occurrence threshold τ_cooc | 1 (that is, zero co-occurrence triggers retrieval) |
| Co-occurrence window | 1,000 tokens |
| Entity/triplet extractor | Qwen2.5-0.5B-Instruct fine-tuned on 40K GPT-4o-mini labels (89.9 F1) |
| Retriever | BM25 over the Wikipedia dump (about 21M passages), top-3 |
| Eval sets | 1,000 validation questions each from 2WikiMultihopQA and HotpotQA |

## Expected numbers (OLMo-2, EM)

| Model | 2Wiki | HotpotQA |
|---|---|---|
| 7B | 32.7 | 35.3 |
| 13B | 41.7 | 35.0 |
| 32B | 46.8 | 41.6 |

These are 5–12 EM points above the best dynamic-RAG baseline (FLARE, DRAGIN, ETC, SeaKR) for each size. The method averages 1.70 retrievals and 1.84 LLM calls per question.

## What to watch

- **Transfer to closed models.** For Llama, Qwen and GPT, the OLMo-2 corpus is used as a *proxy* for their unknown pre-training data. It still helps (up to +14 EM reported), but the proxy is only as good as the overlap between corpora.
- **Aliases.** "NYC" and "New York City" are counted separately, which causes spurious retrievals. This is one of the paper's stated limitations.
