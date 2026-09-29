# Agentic-R: Learning to Retrieve for Agentic Search

| | |
|---|---|
| **Authors** | Wenhan Liu, Xinyu Ma, Yutao Zhu, Yuchen Li, Daiting Shi, Dawei Yin, Zhicheng Dou |
| **Venue / status** | **Findings of ACL 2026**, pp. 15987–16005 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.785/) |
| **Section** | 4 and 18, Retrievers for agents |
| **Verified** | Anthology abstract (September 2026) |

**Problem.** Search agents (Search-R1 and its successors) train the *policy* and keep an off-the-shelf retriever. But agent sub-queries differ from human queries, and what makes a passage useful to an agent mid-trajectory is not the same as topical relevance.

**Method.** Measure passage utility with **two signals**: *local* query–passage relevance and *global* answer correctness of the full multi-turn trajectory. Then **optimise the agent and the retriever bidirectionally and iteratively**: a better retriever changes the agent's trajectories, which changes the retriever's training signal.

**Result.** Consistent improvements over existing retrievers on seven benchmarks.

**Why it matters.** It is the retriever-side answer to The Retrieval Bottleneck. If the ceiling is retrieval, **train the retriever for the agent**. Related work: R3 (RL-trained retriever, arXiv:2510.24652), Critic-R (critic-guided retriever feedback, arXiv:2606.00590), and LatentRAG's jointly trained retriever. See [docs/18](../../docs/18-retrievers-for-reasoning-and-agents.md).
