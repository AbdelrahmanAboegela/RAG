# HiGoE: Hierarchical Graph of Evidence to Enhance Retrieval-Augmented Generation for Long-context Summarization

| | |
|---|---|
| **Authors** | Long Yuan, Kaiwen Tian, Zi Chen, Bolong Zheng, Chuan Ma |
| **Venue / status** | **ACL 2026 main** (Long), pp. 19703–19724 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.902/) · [code](https://github.com/tkw123/HiGOE) · [reproduction guide](../../experiments/higoe.md) |
| **Section** | 7, Knowledge representation |
| **Verified** | Abstract on the ACL Anthology, and pipeline from the repo README (September 2026). We did not verify specific metric values |

**Task.** Long-context **summarization**, not QA. Datasets: QMSum, WCEP, BookSum, GovReport, SQuALITY.

**Problem.** Feeding a long input to an LLM causes attention dilution and hallucination. Chunk-based RAG for summarization picks unreliable, redundant chunks.

**Method.**
1. Build a filtered **proposition–evidence graph**: claims, linked to the source spans that support them.
2. Organise it **hierarchically with Personalized PageRank**.
3. Model relations with an **enhanced Graph Attention Network** that selects evidence for the summariser.

**Result.** It "consistently surpasses baselines in quality and efficiency" (abstract). Open the paper's tables before quoting ROUGE or BERTScore figures.

**What changed.** It brings the graph-RAG idea (structured, deduplicated evidence) to **summarization**, where "what to retrieve" means "which claims cover the document".
