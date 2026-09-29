# SPARKLE: A Structured and Plug-and-play Agentic Retrieval Policy for Adaptive RAG Models

| | |
|---|---|
| **Authors** | Jinyuan Fang, Zaiqiao Meng, Craig Macdonald (University of Glasgow) |
| **Venue / status** | **ACL 2026 main** (Long), pp. 38699–38719 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1793/) · [code](https://github.com/jyfang6/sparkle) · [reproduction notes](../../experiments/sparkle.md) |
| **Section** | 4, Learned retrieval policies (plug-and-play variant) |
| **Verified** | Full text read from the ACL PDF (September 2026) |

**TL;DR.** Instead of fine-tuning the big LLM to search, SPARKLE trains a **small 3B proxy policy** that controls retrieval for a *frozen* reader LLM and a *frozen* retriever. The proxy reasons over a **knowledge-graph-style chain** of triplets extracted from the LLM's thoughts and the retrieved documents. It gains +9.17% (in-domain) and +2.85% (out-of-domain) on average over the strongest adaptive-RAG baselines.

**Problem.** Adaptive RAG either relies on a frozen LLM's own judgement (FLARE, DRAGIN; no supervision) or fine-tunes the LLM (Search-R1; costly, and tied to one model).

**Method.**
- The proxy plays several agent roles in a multi-agent MDP, including **Query Formulation** (find the gap in the KG-based reasoning chain and write a query) and **Knowledge Integration** (pick the triplet that best fills the most important gap and add its source document to the context).
- Triplets are extracted with Llama-3, precomputed and cached, following the authors' earlier KiRAG work.
- Training uses **PPO** with the retriever and LLM treated as the environment, **binary tree-structured rollouts** with pruning for exploration, and Monte-Carlo credit assignment from a single system-level reward.

**Setup.** E5 retriever, Qwen2.5-7B-Instruct reader, Qwen2.5-3B-Instruct proxy. In-domain: HotpotQA, 2Wiki, NQ. Out-of-domain: MuSiQue, Bamboogle, TriviaQA, ASQA. It transfers to BGE and DeepSeek-R1-Distill-Qwen-14B without retraining.

**Limitations (stated).** It depends on triplet quality. GRPO is untried. Only a 3B proxy is tested.

**What changed.** Retrieval control becomes a **separate, portable module**, trained once and reused across LLMs and retrievers.
