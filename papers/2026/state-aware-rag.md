# State-Aware RAG: "Reasoning with Memory: Adaptive Information Management for Retrieval-Augmented Generation"

| | |
|---|---|
| **Authors** | Hieu Man (University of Oregon; work done during an Amazon internship), Ro-ee Tal, Abhishek Kumar, Jaejin (JJ) Cho, Benjamin Hsu (AWS AI) |
| **Venue / status** | **Findings of ACL 2026** |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.1834/) · [Amazon Science page](https://www.amazon.science/publications/reasoning-with-memory-adaptive-information-management-for-retrieval-augmented-generation) · code: [amazon-science/state-aware-rag](https://github.com/amazon-science/state-aware-rag) (linked in the paper) |
| **Section** | 6, Memory and state |
| **Verified** | Full text read from the Amazon Science PDF (September 2026) |

> **Naming:** "State-Aware RAG" is the method name. The paper's title is "Reasoning with Memory: …". Cite the paper by its title.

## TL;DR
Most multi-hop RAG work improves **what gets retrieved**. This paper improves **what the system keeps**. A small trained *extractor* maintains an explicit working memory that is filtered, consolidated and updated after every hop, while the retriever and generator stay frozen. It gains +8.6% over the best memory-augmented baseline (HippoRAG 2) and +9.3% over the best RL-enhanced baseline (s3).

## 1. Problem and gap
In iterative RAG, retrieved text is **appended**. Over 5–10 hops, irrelevant, redundant and contradictory passages pile up, and the context degrades. Prior fixes are static: reranking once, compressing once (RECOMP, LongLLMLingua), a fixed knowledge graph (HippoRAG), or global compression (MemoRAG). None of them curates memory **per step** as the reasoning state changes.

## 2. Key idea
Borrow the cognitive-science idea of **working memory** (Baddeley & Hitch, 1974): a persistent workspace that is actively managed. Make the *manager* the only trained component.

## 3. Method
- **Loop:** sub-question generation → retrieval → **extractor filters and consolidates** → response generation → **memory update**. These are expansion actions A1–A5.
- **Two inference modes:** *Socratic planning* (one iterative chain, cheap) and *MCTS* over reasoning paths with a globally shared memory (more accurate, costly).
- **Path-Outcome Dual Reward:** a *path reward* scores the coherence and sufficiency of the curated memory at each step, and an *outcome reward* scores the final answer. They are combined into a cumulative weighted objective. Both are computed with an LLM-as-judge.
- **Training:** SFT on about 10K successful reasoning paths (5–10 steps each, about 70K state-action pairs), then **GRPO** with the dual reward.
- **Components:** extractor Qwen3-4B (trained); generator Qwen3-8B (frozen); retriever Qwen3-Embedding-4B over the 2023 Wikipedia dump (frozen).

## 4. Results
- **Benchmarks (8):** multi-hop 2Wiki, HotpotQA, MuSiQue, Bamboogle; single-hop SimpleQA, NQ, TriviaQA, PopQA. 1,000 samples each (all 125 for Bamboogle).
- **Multi-hop:** 58.0% average accuracy, **+8.6%** over HippoRAG 2.
- **Single-hop:** 72.7%, **+9.3%** over s3.
- **Plug-and-play:** a stronger generator (Qwen3-8B → Qwen3-30B-A3B) gives +7.4% without retraining the extractor. **Replacing Wikipedia with Google Search gives +22.2%**, a striking data point for the "retrieval is the bottleneck" argument.
- **Ablation:** path-only and outcome-only rewards both underperform the dual reward.

## 5. Limitations
- **(stated)** The LLM-judge rewards make RL training expensive.
- **(stated)** Retrieval quality bounds everything (see the +22.2% from Google Search).
- **(stated)** It is untested outside QA, for example on scientific or enterprise documents.
- **(stated)** The MCTS mode is costly.

## 6. What changed vs. the previous approach
It shifts attention from **information acquisition** to **information management**: memory is a trained, stateful component, not a growing context window.

## 7. Discussion questions
1. The retriever and generator are frozen and only a 4B extractor is trained. Why might that generalise better than training the generator end-to-end (as in Search-R1)?
2. What would a *non-LLM-judge* path reward look like?
3. Relate this to [SPARKLE](sparkle.md), which also trains only a small proxy model. What does each proxy control?
