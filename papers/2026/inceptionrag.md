# InceptionRAG: Stealthy Poisoning Attack Against Retrieval-Augmented Generation

| | |
|---|---|
| **Authors** | Jiachang Zhang, Min Chen, Xiao Ren, Zhenyong Zhang, Yuanchao Shu, Yunjun Gao, et al. |
| **Venue / status** | **ACM CCS 2026** (to appear, per the arXiv comment) |
| **Links** | [arXiv:2609.16818](https://arxiv.org/abs/2609.16818) |
| **Section** | 15, Security |
| **Verified** | arXiv abstract (September 2026) |

**Idea.** Earlier poisoning attacks (PoisonedRAG) put the whole malicious payload in **one** document, and defenses learned to spot such documents. InceptionRAG **fragments the payload into a chain of harmless-looking passages**. Each one passes inspection on its own, but when they are retrieved together, the LLM **deduces the target misinformation itself through multi-hop reasoning**.

**Black-box automation.** Zeroth-order suffix optimisation (ZOSO) generates "authoritative" suffixes without model access.

**Results.** >80% attack success across three datasets and three LLMs, bypassing defenses designed for single-document injection.

**The paradox.** *Stronger reasoning makes the model more vulnerable:* the better it chains facts, the better the attack works.

**Defense proposed.** **HODOR**, a document-isolation defense that decouples logical dependencies between retrieved passages.

**Why it matters for this repo.** Multi-hop RAG, the topic of Sections 4–7, is exactly the capability this attack exploits. See [docs/15](../../docs/15-security.md).
