# QueryLink: Leveraging Query-Memory Alignment for Long-Term Reasoning in LLM Agents

| | |
|---|---|
| **Authors** | Xuxian Hu, Zhu Teng, Wei Zhang, Ming He, Jianping Fan |
| **Venue / status** | **Findings of ACL 2026** |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.765/) · [code](https://github.com/Dontplay0112/querylink) · [reproduction guide](../../experiments/querylink.md) |
| **Section** | 6, Memory and state |
| **Verified** | Anthology abstract and repo README (September 2026) |

**Problem.** In long-term conversational memory, a **user query and the stored memory it needs are phrased very differently**. "What did I say I'd cook for Anna?" should match "Planning lasagna for Anna's birthday", three weeks earlier. Fixed-size memory chunks also cut conversations mid-thought.

**Method.**
- **Query-Memory Alignment:** dual-side, multi-view projection of queries *and* memories into a shared semantic space. Both sides are rewritten or represented from several views, instead of just embedding the query.
- **Coherent Memory Chunking:** memory is segmented by semantic coherence across turns, not fixed windows.

**Results.** At least +7% reasoning accuracy on **LoCoMo** and **LongMemEval**, and >6% F1 and BLEU-1 when added to **A-MEM**.

**Why it's in a RAG repo.** Agent memory *is* retrieval, over the agent's own history. The query–document gap is the old IR vocabulary-mismatch problem (compare HyDE and query rewriting in [docs/01](../../docs/01-foundations.md)) in a new setting.
