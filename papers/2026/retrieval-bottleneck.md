# The Retrieval Bottleneck: Scaling Laws for Reinforcement Learning in RAG

| | |
|---|---|
| **Authors** | Shu Zhou, Jinman Leng, Yufei Song, Xin Wang, Tao Fan, Hao Wang |
| **Venue / status** | **ACL 2026 main** (Long), pp. 32045–32069 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1478/) · code: not linked |
| **Section** | 4, Learned retrieval policies (the "so what" slide) |
| **Verified** | Abstract only (September 2026). Read the full paper before presenting its curves |

**TL;DR.** The first systematic study of how RL for RAG *scales*. Performance follows **sigmoidal scaling curves** in RL compute, and the **asymptote is set by retrieval quality**, not by RL compute or algorithm choice.

**Three principles (from the abstract).**
1. **Retrieval quality bounds achievable performance.** A better retriever gives larger gains than algorithmic changes.
2. **Design choices** (objective, reward, off-policy tricks) mostly change *compute efficiency*, with smaller effects on the ceiling.
3. **Stable configurations extrapolate:** 3.1% error when predicting performance at 4× compute.

It also reports that the optimal number of documents grows during training, and that how well an RL algorithm works depends on retrieval quality. The resulting recipe is called **RAG-ScaleRL**.

**Why it matters.** It explains a pattern that recurs in this repo: State-Aware RAG gains +22.2% just by switching Wikipedia for Google Search, and Search-R1-style papers keep improving by changing the retriever. **Before tuning the RL algorithm, fix retrieval.**
