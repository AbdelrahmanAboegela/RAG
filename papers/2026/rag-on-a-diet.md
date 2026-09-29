# RAG-on-a-Diet: A Reinforcement Learning-Based Dynamic Resource Optimization Framework for RAG

| | |
|---|---|
| **Authors** | Hongwen Ding, Yizheng Zhao |
| **Venue / status** | **ACL 2026 main** (Long) |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1562/) · code: not linked |
| **Section** | 4, Learned retrieval policies (cost-aware) / 10, Efficiency |
| **Verified** | Abstract on the ACL Anthology (September 2026) |

**TL;DR.** RAG-on-a-Diet treats **each hop** of a multi-hop pipeline as its own decision and uses an RL agent to choose **which model size** to spend on it (Qwen3-4B, Qwen3-30B or DeepSeek-R1-671B). Decisions use entity- and confidence-aware features and a two-tier termination policy.

**Results (from the abstract).**
- 60.07% lower monetary cost than IRCoT, for a 3.7% F1 drop on HotpotQA.
- Matches Adaptive-RAG's F1 at 37.30% lower cost.
- Up to 2.33× higher quality per dollar.
- Evaluated on HotpotQA, MuSiQue, 2Wiki, CRAG and Bamboogle.

**What changed.** AutoSearch saves cost by taking **fewer hops**; RAG-on-a-Diet saves it by making **each hop cheaper**. The two are complementary.

**Discussion.** Money is a better cost unit than the number of searches when models of very different sizes are mixed. Why don't most papers report it?
