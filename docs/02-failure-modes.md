# 2. Why vanilla RAG fails

"Retrieve top-k, then generate" breaks in five predictable ways. Each failure motivates a line of work in later sections.

| Failure | Evidence | Addressed in |
|---|---|---|
| Multi-hop needs information that the first query can't reach | the running example; HotpotQA, 2Wiki, MuSiQue | §3 IRCoT, §4 Search-R1 and successors, §7 T²RAG |
| Irrelevant context hurts | Yoran et al. 2024; Jin et al. 2025 | §3 CRAG, Chain-of-Note; §6 State-Aware RAG |
| Position effects | Lost in the Middle | reranking, evidence packing (§7 HiKEY) |
| Context vs. memory conflicts | Knowledge-conflicts survey; ClashEval | §8 FRANQ, CMC-Bench |
| Adversarial / poisoned corpora | PoisonedRAG, BadRAG | §8 |

## 2.1 Multi-hop: the first query can't reach the answer

In the running example, the question mentions two films but the answer depends on two *people* the question never names. No single embedding of the question is close to "Jean-Daniel Pollet was a French filmmaker". Run `python code/examples/01_hybrid_retrieval.py`: BM25, dense and hybrid retrieval all return the film pages and miss both nationality pages. **Multi-hop requires the output of one retrieval to form the next query.** That is the whole motivation for iterative and agentic RAG.

## 2.2 Noise: irrelevant context actively hurts

Retrieval is imperfect, and irrelevant passages don't just waste tokens: they can pull accuracy **below the no-retrieval baseline** (Yoran et al., ICLR 2024, [arXiv:2310.01558](https://arxiv.org/abs/2310.01558)). With long-context models, adding more retrieved passages first helps and then hurts, because *hard negatives* (topically similar but wrong passages) distract the model (Jin et al., ICLR 2025, [arXiv:2410.05983](https://arxiv.org/abs/2410.05983)). In iterative RAG, noise **compounds** across hops, which is the core argument of State-Aware RAG.

## 2.3 Lost in the middle

Liu et al. (TACL 2024, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)) moved the one relevant document through a 20-document context. Accuracy was highest when it was first or last and lowest in the middle, a **U-curve**, sometimes below closed-book. Mitigations include reranking so the best evidence is first, keeping k small, reordering, and structured packing (HiKEY's governing headers).

## 2.4 Knowledge conflicts

Retrieved text can contradict the model's parametric knowledge, or other retrieved text.
- **Context–memory conflict:** does the model follow the context or its prior? ClashEval ([arXiv:2404.10198](https://arxiv.org/abs/2404.10198)) shows that models adopt wrong context surprisingly often, and more often when their prior is weak.
- **Inter-context conflict:** two retrieved sources disagree (stale versus fresh, rumour versus fact).
- **Multimodal conflict:** text versus image. CMC-Bench (2026) finds VLMs either abstain or fabricate.
- Taxonomy: Xu et al., EMNLP 2024 ([arXiv:2403.08319](https://arxiv.org/abs/2403.08319)).

A subtle consequence, formalised by **FRANQ** (2026): "not supported by the context" ≠ "false". Evaluation that equates the two penalises correct parametric knowledge.

## 2.5 Corpus poisoning

If attackers can write to the corpus (the web, a wiki, a shared drive), they can control answers. **PoisonedRAG** ([arXiv:2402.07867](https://arxiv.org/abs/2402.07867)) reaches about a 90% attack success rate by injecting about 5 crafted passages per target question into a corpus of millions. Agentic systems widen the attack surface: the SoK on agentic RAG lists *memory poisoning* and *cascading tool-execution vulnerabilities* as systemic risks. See [08](08-evidence-and-trust.md).

## 2.6 Cost

Every retrieval adds latency. Every retrieved token adds prefill cost. Multi-step agents multiply both: Search-R1 takes 16–22× the inference time of naive RAG (measured in the LatentRAG paper). Cost is a first-class research axis in 2026. See [10](10-efficiency.md).

## Discussion
- Which of these failures can a better *retriever* fix, and which need a better *policy* or *reader*? (Keep this question in mind for The Retrieval Bottleneck in §4.)
