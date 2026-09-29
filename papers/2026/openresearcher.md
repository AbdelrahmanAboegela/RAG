# OpenResearcher: A Fully Open Pipeline for Long-Horizon Deep Research Trajectory Synthesis

| | |
|---|---|
| **Authors** | Zhuofeng Li, Dongfu Jiang, Xueguang Ma, Haoxiang Zhang, Ping Nie, Yuyu Zhang, et al. |
| **Venue / status** | **arXiv** (March 2026) |
| **Links** | [arXiv:2603.20278](https://arxiv.org/abs/2603.20278) · [code, data, checkpoints](https://github.com/TIGER-AI-Lab/OpenResearcher) |
| **Section** | 13, Deep research |
| **Verified** | arXiv abstract (September 2026) |

**Problem.** Training deep-research agents needs long trajectories (search, open, read, reason, 100+ tool calls). Synthesising them against proprietary web APIs is **costly, unstable and irreproducible**.

**Method.**
- Bootstrap a **15M-document offline corpus** once.
- Run the search-and-browse loop entirely offline with three browser primitives: **search, open, find**.
- Use GPT-OSS-120B as the teacher to synthesise **97K+ trajectories**, including a long tail with 100+ tool calls.
- Apply SFT to a 30B-A3B backbone.

**Results.** **54.8% on BrowseComp-Plus**, +34.0 points over the base model, and competitive on BrowseComp, GAIA and xbench-DeepSearch.

**Why it matters.** It is the deep-research counterpart of what Wikipedia-2018 did for QA-RAG: a **shared, instrumented, offline environment**. That enables controlled studies, for example of how retrieval success relates to final accuracy.
