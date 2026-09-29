# HiPRAG: Hierarchical Process Rewards for Efficient Agentic Retrieval Augmented Generation

| | |
|---|---|
| **Authors** | Peilin Wu, Mian Zhang, Kun Wan, Wentian Zhao, Kaiyu He, Xinya Du, et al. |
| **Venue / status** | **ICLR 2026** (per the arXiv comment); arXiv October 2025 |
| **Links** | [arXiv:2510.07794](https://arxiv.org/abs/2510.07794) |
| **Section** | 4, Learned retrieval policies (process rewards) |
| **Verified** | arXiv abstract (September 2026) |

**Problem.** Search agents trained on outcome rewards both **over-search** (look up what they already know) and **under-search** (guess when they should look up).

**Method.**
- Decompose each trajectory into discrete, parsable steps.
- For every step, check *on the fly* whether the search decision was necessary. This is a **knowledge-grounded** check: could the model have answered that step without searching?
- The **hierarchical reward** is format + outcome, plus a bonus proportional to the fraction of optimal search and non-search steps. The bonus is applied only on top of a correct, well-formed answer.

**Results (abstract).** On seven QA benchmarks, average accuracy is **65.4% (3B)** and **67.2% (7B)**. The over-search rate falls to **2.3%**, and the under-search rate also drops. It works across RL algorithms, model families (Qwen2.5, Llama-3.2), sizes and types.

**Relation to AutoSearch.** Both attack search efficiency. **AutoSearch** defines optimal depth *per trajectory* (the first step where the intermediate answer is correct). **HiPRAG** judges *each individual search decision*. AutoSearch uses HiPRAG as a baseline. See [autosearch.md](autosearch.md).
