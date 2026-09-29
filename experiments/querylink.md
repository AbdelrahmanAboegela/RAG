# Reproducing QueryLink

**Repo:** [Dontplay0112/querylink](https://github.com/Dontplay0112/querylink) · **Paper:** [Findings ACL 2026](https://aclanthology.org/2026.findings-acl.765/) · **Notes:** [papers/2026/querylink.md](../papers/2026/querylink.md)

## Setup and run (from the repo README)

```bash
git clone https://github.com/Dontplay0112/querylink.git
cd querylink
uv sync --frozen
cp .env.example .env              # add API keys
uv run python src/prepare.py      # downloads NLP resources

bash run.sh locomo                # needs data/locomo10.json and data/locomo10.pkl
bash run.sh longmemeval           # needs data/longmemeval_s.json
CUDA_VISIBLE_DEVICES=0 bash run.sh locomo
```

The default agent LLM is `gpt-4o-mini`. Settings for the task, model, concurrency and data paths live in `config/`.

## What to watch

- The paper reports ≥7% reasoning-accuracy gains on LoCoMo and LongMemEval, and >6% F1/BLEU-1 gains when QueryLink is added to A-MEM. To reproduce the second number, run [A-MEM](https://github.com/agiresearch/A-mem) with and without QueryLink's alignment on the same LLM.
