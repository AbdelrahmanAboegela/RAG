# Reproducing T²RAG

**Repo:** [Emory-Melody/T2RAG](https://github.com/Emory-Melody/T2RAG) (an earlier copy lives at [rockcor/T2RAG](https://github.com/rockcor/T2RAG)) · **Paper:** [Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1310/) / [arXiv:2508.02435](https://arxiv.org/abs/2508.02435) · **Notes:** [papers/2026/t2rag.md](../papers/2026/t2rag.md)

This is API-based. A single GPU is enough for the NV-Embed-v2 embeddings.

## Setup and run (from the repo README)

```bash
pip install -r requirements.txt

export CUDA_VISIBLE_DEVICES=0
export HF_HOME='~/.hf'
export OPENAI_API_KEY=<your openai api key>
export GOOGLE_API_KEY=<your gemini api key>

python main.py --dataset 2wikimultihopqa --method trag
```

- Datasets: `popqa`, `2wikimultihopqa`, `musique`, `hotpotqa`, `story`, `medical`
- Methods: `trag` (T²RAG), `standard` (chunk RAG), `hippo` (HippoRAG-style baseline)
- Other backends: `main_gemini.py`, `main_oss.py` (open-weight models via HF)
- Outputs: `outputs/<dataset>_<method>`

## What to watch

- **Indexing cost is paid once.** Triplet extraction runs an LLM over every chunk. It is cheaper than GraphRAG-style graph construction, but for a large corpus it is still the dominant cost.
- **Max 3 iterations** in the paper, set for fairness with baselines. Harder datasets may benefit from more.
- **Keep the source chunks.** Removing them costs 26–34% in the ablation, because propositions lose detail.
- A mechanism-level toy of the triplet state machine is in [`code/ragkit/t2rag.py`](../code/ragkit/t2rag.py).
