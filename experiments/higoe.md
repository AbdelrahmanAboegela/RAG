# Reproducing HiGoE

**Repo:** [tkw123/HiGOE](https://github.com/tkw123/HiGOE) · **Paper:** [ACL 2026 main](https://aclanthology.org/2026.acl-long.902/) · **Notes:** [papers/2026/higoe.md](../papers/2026/higoe.md)

HiGoE is for **long-context summarization**, not QA. Its datasets are QMSum, WCEP, BookSum, GovReport and SQuALITY.

## Install (from the repo README)

```bash
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1
pip install dgl==1.0.0+cu113 -f https://data.dgl.ai/wheels/cu113/repo.html
pip install openai==0.28 pandas langchain langchain-core langchain-community
pip install langchain-experimental tiktoken tqdm bert_score rouge_score networkx
pip install faiss-gpu transformers
```

The pins are old (CUDA 11.3, torch 1.12, `openai==0.28`), so use a dedicated environment or container.

## Pipeline

```bash
python graph_construction.py --cuda 0 --dataset [DATASET] --construct_mode claim   # proposition–evidence graph
python knowledge_synthesizer_ppr.py --dataset [DATASET] --cuda 0                  # Personalized PageRank hierarchy
python training_preparation.py --cuda 0 --dataset [DATASET]
python train.py --cuda 0 --dataset [DATASET]                                       # enhanced GAT
python eval.py --cuda 0 --dataset [DATASET]
python sum_eval.py --cuda 0 --file_name ./result/[DATASET].json                    # ROUGE / BERTScore
```
