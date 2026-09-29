# 12. Open problems (as of September 2026)

Each item links to the 2026 evidence that makes it open.

1. **Retrieval sets the ceiling, and RL doesn't lift it.** The Retrieval Bottleneck shows RL for RAG saturates at a level set by retrieval quality. *Open:* co-training retrievers inside the RL loop at scale (LatentRAG trains its retriever, but by SFT); learning the *corpus* (what to index) as well as the policy.

2. **Process rewards without gold evidence.** AutoSearch needs exact-match intermediate answers; State-Aware RAG needs an expensive LLM judge; StepSearch needs gold evidence. *Open:* cheap, verifiable step rewards for long-form and open-ended tasks.

3. **Beyond short-answer QA.** Nearly all RL-search results are on 7 factoid datasets. *Open:* long-form answers, enterprise documents, multilingual corpora, deep-research reports. Evaluation there (BrowseComp, FRAMES, CRAG) is still thin.

4. **Latent vs. auditable.** LatentRAG cuts latency by about 90% but hides the queries. *Open:* latent RL; guarantees that decoded latents match what was actually searched; regulatory acceptability.

5. **When to retrieve, grounded in data.** QuCo-RAG uses pre-training statistics, but closed models don't disclose their corpora and proxies degrade. *Open:* estimating a closed model's knowledge boundary from outside; combining corpus signals with RL policies.

6. **Memory management at scale.** State-Aware RAG curates memory within an episode; QueryLink aligns queries across sessions. *Open:* unified memory that spans both; forgetting and updating; memory poisoning defences.

7. **Structure without heavy indexing.** T²RAG and HiKEY show structure helps. *Open:* incremental indexing for changing corpora (both list this as a limitation); robustness to parsing errors.

8. **Multimodal reading, not just retrieval.** Chart-MRAG: ≤71% correctness even with gold retrieval. CMC-Bench: models abstain or fabricate on conflicts. HiKEY: recall +12.9% but QA only +6.8%. *Open:* chart and table reasoning; modality arbitration.

9. **Trust.** FRANQ separates factuality from faithfulness. *Open:* calibrated abstention in agentic loops; provenance across many hops; defences against poisoning and prompt injection in retrieved content.

10. **Cost as a first-class objective.** AutoSearch (depth), RAG-on-a-Diet (model size) and SpecCache (prefill) each optimise one axis. *Open:* joint optimisation, and reporting cost in money on shared hardware.

11. **Reasoning makes attacks easier.** InceptionRAG (CCS 2026) shows multi-hop reasoning can be steered by harmless-looking passage chains. *Open:* defenses that don't disable the multi-hop reasoning we want (see [15](15-security.md)).

12. **Deep research evaluation and credit assignment.** FINDER/DEFT shows agents fail at evidence integration and verification. MiroEval shows the process predicts the outcome. *Open:* process rewards for 100+-call horizons; citation faithfulness at report scale (see [13](13-deep-research.md)).

13. **Retrievers that serve agents.** Agentic-R, R3 and Critic-R train retrievers for agent sub-queries. *Open:* stable co-training at scale; retrievers robust to biased queries (CoRM-RAG).

14. **Interpretability of evidence use.** Attribution graphs (arXiv:2605.14192) separate successful from failed evidence flow, and ParallaxRAG exploits head specialisation. *Open:* using internal signals as cheap, reliable retrieval triggers or error detectors in production.

## Research idea prompts
- An **AutoSearch-style depth reward for long-form answers**, using claim-level coverage (FRANQ-style) instead of exact match.
- **QuCo-RAG signals as RL features:** give the search policy corpus frequency as an input.
- **A latent version of T²RAG:** triplet placeholders as latent slots.
- **A HiKEY-style hierarchy for agent memory:** sessions › topics › facts.
