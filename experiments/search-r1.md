# Reproducing Search-R1

**Repo:** [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1) · **Paper:** [arXiv:2503.09516](https://arxiv.org/abs/2503.09516) · **Notes:** [papers/2025/search-r1.md](../papers/2025/search-r1.md)

Search-R1 is the de-facto base for 2025–26 RL search work: AutoSearch builds on it, and LatentRAG distils its trajectories. If you only reproduce one system, reproduce this one.

## 1. Environments (from the repo README)

```bash
# policy / training env
conda create -n searchr1 python=3.9
conda activate searchr1
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121
pip3 install vllm==0.6.3
pip install -e .
pip3 install flash-attn --no-build-isolation
pip install wandb

# retriever env (separate, because faiss-gpu pins conflict)
conda create -n retriever python=3.10
conda activate retriever
conda install pytorch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 pytorch-cuda=12.1 -c pytorch -c nvidia
pip install transformers datasets pyserini
conda install -c pytorch -c nvidia faiss-gpu=1.8.0
pip install uvicorn fastapi
```

## 2. Corpus, index and data

```bash
save_path=/the/path/to/save
python scripts/download.py --save_path $save_path
cat $save_path/part_* > $save_path/e5_Flat.index
gzip -d $save_path/wiki-18.jsonl.gz
python scripts/data_process/nq_search.py
```

The flat E5 index over 21M passages needs about 60–65 GB of RAM (or GPU memory with faiss-gpu). On a small machine, switch to the BM25 retriever or an HNSW index.

## 3. Launch the retriever, then train

```bash
conda activate retriever
bash retrieval_launch.sh          # starts a FastAPI server that rollouts query

conda activate searchr1
bash train_ppo.sh                 # or: bash train_grpo.sh
```

## 4. Inference

```bash
python infer.py
```

## What to watch

- **Reward** is exact match on the final `<answer>` only (outcome reward). There is no format or process reward in the original recipe. Later papers (AutoSearch, StepSearch, UR²) add these.
- **Retrieved-token masking** is on by default. If you turn it off, training becomes unstable because the policy is pushed to "predict" retrieved text.
- **PPO vs GRPO:** the paper reports GRPO converging faster but less stably; PPO is the safer default.
- **Base vs Instruct:** both work. Base models need more steps to learn the format.
- A mechanism-level toy of the rollout loop is in [`code/ragkit/agentic.py`](../code/ragkit/agentic.py).
