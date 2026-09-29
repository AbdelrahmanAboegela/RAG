# 15. Security and privacy of RAG systems

RAG adds an **external knowledge access path** to an LLM. Everything on that path can be attacked: the corpus, the index, the retriever, the retrieved text entering the prompt, shared caches, and agent memory.

## 15.1 A taxonomy: SLOT

*Securing Retrieval-Augmented Generation: A Taxonomy of Attacks, Defenses, and Future Directions* ([arXiv:2604.08304](https://arxiv.org/abs/2604.08304), 2026) organises the literature on four axes over a six-stage knowledge-access pipeline:

- **S**urface: where the adversary acts (corpus, index, query, retrieved context, output, ...)
- **L**ayer: which defense layer controls that point
- **O**bjective: which property breaks (confidentiality, integrity or availability)
- **T**arget: a single known query (T1), or manipulating a *claim* across a query distribution (T2)

Paper list: [TreeAI-Lab/Awesome-RAG-Security](https://github.com/TreeAI-Lab/Awesome-RAG-Security).

## 15.2 Integrity attacks: corpus poisoning

| Attack | Idea | Result |
|---|---|---|
| **PoisonedRAG** (USENIX Sec 2025; [arXiv:2402.07867](https://arxiv.org/abs/2402.07867)) | craft ~5 passages per target question that are (a) retrievable and (b) induce the target answer | ~90% attack success rate in a corpus of millions |
| **BadRAG** ([arXiv:2406.00083](https://arxiv.org/abs/2406.00083)) | trigger-activated poisoned passages | backdoor-style control |
| **InceptionRAG** (**CCS 2026**; [note](../papers/2026/inceptionrag.md)) | split the payload across **harmless-looking passages**; the LLM *reasons its way* to the misinformation | >80% ASR; evades single-document defenses; *stronger reasoning = more vulnerable* |
| Relevance-based sycophancy (CoRM-RAG, [arXiv:2605.01302](https://arxiv.org/abs/2605.01302)) | no attacker needed: a *biased query* retrieves evidence that confirms its false premise | the relevance–robustness gap |

## 15.3 Prompt injection through retrieved content

**Indirect prompt injection:** a retrieved page contains instructions ("ignore previous instructions and ..."). In RAG this is the more dangerous variant, because the attacker never talks to the model directly. Agentic and deep-research systems read thousands of pages and can *act* (tools), so the impact is larger. The SoK on agentic RAG lists *cascading tool-execution vulnerabilities* and *memory poisoning* as systemic risks.

## 15.4 Confidentiality: leaking the corpus and other users' data

- **Knowledge extraction:** crafted queries make the model regurgitate private documents verbatim.
- **KV-cache side channels:** **SpliceLeak** ([arXiv:2606.21842](https://arxiv.org/abs/2606.21842), 2026) shows that *non-prefix* KV-cache fusion (vLLM + LMCache) leaks, through TTFT timing, first the length and then the **content** of other users' private prompts, up to 100% extraction in bounded-entropy settings. The proposed mitigation is chunk padding plus constant-time boundary fusion. **Cross-tenant cache sharing is a privacy decision, not only a performance one.**
- **Answer caches** can serve one user's answer to another. Scope caches per tenant or permission set ([`cache.py`](../code/ragkit/cache.py)).

## 15.5 Defenses (none is complete)

| Layer | Defense | Examples |
|---|---|---|
| Ingestion | source allow-lists, provenance, signing, trust tiers | — |
| Retrieval | retrieve wider to dilute poison; perplexity and similarity filters | **RAGuard** ([arXiv:2510.25025](https://arxiv.org/abs/2510.25025)) |
| Retrieval | robust aggregation: answer from isolated subsets, then vote | isolate-then-aggregate designs; **HODOR** document isolation (InceptionRAG paper) |
| Detection | attribute the answer to influential tokens or documents | **TRACE** ([arXiv:2606.25721](https://arxiv.org/abs/2606.25721), EMNLP 2026 Industry) |
| Generation | treat retrieved text as data; separate instruction and data channels; refuse to follow instructions inside documents | system-prompt design, structured prompts |
| Agent | least-privilege tools, human confirmation for side effects, memory write validation | — |
| Serving | per-tenant caches, constant-time cache fusion | SpliceDefense |

As of 2026 there is **no published defense that makes corpus poisoning a solved problem**. The KDD 2026 tutorial states the same: adversarial robustness remains open and no existing defense is universally robust.

## 15.6 Checklist for a production RAG system
- [ ] Who can write to the corpus? Log and review writes.
- [ ] Is every chunk traceable to a source and a version?
- [ ] Are document permissions enforced **at retrieval time**, not in the prompt?
- [ ] Are retrieved passages wrapped and labelled as untrusted data?
- [ ] Can the agent take irreversible actions based on retrieved text?
- [ ] Are KV and answer caches scoped per tenant?
- [ ] Do you red-team with PoisonedRAG-style and split-payload (InceptionRAG-style) injections?
