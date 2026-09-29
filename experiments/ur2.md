# Reproducing UR²

**Repo:** [Tsinghua-dhy/UR2](https://github.com/Tsinghua-dhy/UR2) · **Paper:** [ACL 2026 main](https://aclanthology.org/2026.acl-long.580/) / [arXiv:2508.06165](https://arxiv.org/abs/2508.06165) · **Models:** [ModelScope UR2 collection](https://www.modelscope.cn/collections/UR2-9471aa070f1a46) · **Notes:** [papers/2026/ur2.md](../papers/2026/ur2.md)

**Compute in the paper:** 8×A100, about 160 GPU-hours per run (up to 2 epochs), learning rate 2e-6, at most 4 retrieval turns.

## 1. Environment (from the repo README)

```bash
git clone https://github.com/Tsinghua-dhy/UR2.git
cd UR2
conda env create -f environment.yaml
conda activate ur2
pip install flash-attn==2.7.4.post1
cd UR2_RL/OpenRLHF-RAG && pip install --no-deps -e .
```

Pinned versions matter: `flagembedding==1.3.4`, `flash-attn==2.7.4.post1`, `vllm==0.6.5`.

## 2. Corpus and index

1. Download the Wikipedia abstract and full-text corpora and the BGE embedding model.
2. Preprocess:
   ```bash
   python process_enwiki_full_split_kilt_to_100.py
   python process_enwiki_abstract.py
   ```
3. Embed and index (HNSW):
   ```bash
   python build_corpus_embedding_abstract.py
   python build_corpus_index_hnsw.py
   ```

## 3. Training

```bash
bash load_all_corpus.sh
bash start_gpt_4.1_suammry_search_o1.sh     # LLM summariser used by "hybrid knowledge access"
cd ./UR2_RL/train && bash start_reward_qwen_7b_medqa_mmlu.sh
cd ./UR2_RL/scripts
bash ray_start.sh
bash start_train.sh
bash merge_model.sh
```

The summariser script calls an external LLM API (GPT-4.1 in the script name). Budget for it, or point it at a local model.

## 4. Evaluation

```bash
cd ./eval/eval_scripts
bash eval_mmlupro_multiturn_search_o1.sh
```

## What to watch

- **Two RL stages.** Stage 1 (about 10 steps) rewards *using* retrieval (+3 for one query, +4 for several) so the model does not collapse to pure chain-of-thought. Stage 2 switches to answer correctness (+2) plus format (+1). If you skip stage 1, expect retrieval usage to die out on math and MMLU-Pro.
- **Curriculum.** Difficulty comes from 20 rollouts per question: easy (0.8–1.0), medium (0.5–0.8), hard (0.2–0.5). Retrieval prompting is enabled only for hard math items; open-domain QA always retrieves.
- **Algorithm:** REINFORCE++ via OpenRLHF, not PPO/GRPO via verl, so hyperparameters do not transfer directly from Search-R1.
