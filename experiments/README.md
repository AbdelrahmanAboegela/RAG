# `experiments/`: reproducing the papers with their official code

This folder tells you how to run each paper's **official** code: where the repo is, what hardware it needs, what the entry points are, and what to watch for. Commands are copied from each repository's README as of **September 2026**. Repositories change, so treat the upstream README as the source of truth.

| Guide | Official repo | Needs GPU for | Difficulty |
|---|---|---|---|
| [Search-R1](search-r1.md) | [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1) | RL training (≥1×A100 80GB for 3B; 8×A100 comfortable for 7B), retriever index | ★★★ |
| [UR²](ur2.md) | [Tsinghua-dhy/UR2](https://github.com/Tsinghua-dhy/UR2) | RL training (paper: 8×A100, ~160 GPU-h) | ★★★ |
| [AutoSearch](autosearch.md) | [bofusun/AutoSearch](https://github.com/bofusun/AutoSearch) | RL training (verl-based, Qwen2.5-3B/7B) | ★★★ |
| [QuCo-RAG](quco-rag.md) | [ZhishanQ/QuCo-RAG](https://github.com/ZhishanQ/QuCo-RAG) | inference only (OLMo-2 7B–32B); Elasticsearch | ★★ |
| [T²RAG](t2rag.md) | [Emory-Melody/T2RAG](https://github.com/Emory-Melody/T2RAG) | API-based (OpenAI / Gemini); embeddings | ★ |
| [HiGoE](higoe.md) | [tkw123/HiGOE](https://github.com/tkw123/HiGOE) | GNN training + OpenAI API | ★★ |
| [QueryLink](querylink.md) | [Dontplay0112/querylink](https://github.com/Dontplay0112/querylink) | API-based (gpt-4o-mini default) | ★ |
| [SPARKLE](sparkle.md) | [jyfang6/sparkle](https://github.com/jyfang6/sparkle) | PPO on a 3B proxy model | ★★★ |
| [Chart-MRAG Bench](chart-mrag.md) | [Nomothings/CHARGE](https://github.com/Nomothings/CHARGE), HF `ymyang/chart-mrag` | MLLM inference | ★ |

Papers with **no public code** as of September 2026 (checked on the paper page and by search): LatentRAG, State-Aware RAG (the paper footnote points to [amazon-science/state-aware-rag](https://github.com/amazon-science/state-aware-rag); the repo exists, but check whether it contains code yet), HiKEY, FRANQ (method builds on [LM-Polygraph](https://github.com/IINemo/lm-polygraph)), SpecCache, RAG-on-a-Diet, The Retrieval Bottleneck, EgoMemory, CMC-Bench.

## Shared building blocks

Most RL-search papers reuse the same pieces, so it pays to set these up once:

- **Corpus:** the 2018 Wikipedia dump (21M 100-word passages, from DPR), distributed by FlashRAG and Search-R1 as `wiki-18.jsonl`.
- **Retriever:** E5-base-v2 with a FAISS flat index (`e5_Flat.index`), or BM25 via Pyserini. Serve it as a small FastAPI service so that rollout workers can call it.
- **Datasets:** NQ, TriviaQA, PopQA (single-hop); HotpotQA, 2WikiMultihopQA, MuSiQue, Bamboogle (multi-hop). [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG) packages all of them in one format.
- **RL framework:** [verl](https://github.com/volcengine/verl) (Search-R1, AutoSearch) or [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) (UR²). Both use vLLM for rollouts.

## Fair-comparison checklist

Before you put two papers' numbers side by side (see [docs/11-evaluation.md](../docs/11-evaluation.md)):

- [ ] Same backbone **and** variant (Base vs Instruct changes Search-R1 results a lot).
- [ ] Same retriever, corpus and top-k.
- [ ] Same test split and sample size. Many papers use a random 1,000-example subset, and Bamboogle has only 125 questions, so ±1 question is ±0.8 EM.
- [ ] Same metric definition (EM vs cover-EM vs F1 vs LLM-judge accuracy).
- [ ] Same maximum number of search turns.
- [ ] Latency measured on the same hardware, with the same batch size.
