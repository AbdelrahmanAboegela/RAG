# Lecture outline: "Advanced RAG: from pipelines to learned policies"

**Assumed format:** one lecture for a graduate audience; 3 hours (about 115 slides) or 90 minutes (about 60 slides). Budget 1–1.5 minutes per slide. Put **"as of September 2026"** on the title slide.

**Thesis:** RAG is shifting from a pipeline you engineer to a policy the model learns.
**Four questions:** when to retrieve, what to retrieve, how to use it, at what cost.
**Running example:** *Are the directors of Move (1970) and Méditerranée (1963) from the same country?* (see [00-overview](00-overview.md)). Replace it with a question from your audience's domain if you can.

| # | Section | Slides 3 h / 90 min | Content | Docs |
|---|---|---|---|---|
| 0 | Motivation | 6 / 4 | hallucination, staleness, the thesis, the running example | [00](00-overview.md) |
| 1 | Foundations | 12 / 4 | pipeline, sparse/dense/hybrid, chunking, reranking | [01](01-foundations.md) |
| 2 | Why vanilla RAG fails | 8 / 4 | multi-hop, noise, lost-in-the-middle, conflicts, poisoning | [02](02-failure-modes.md) |
| 3 | The toolkit you need first | 14 / 8 | Self-RAG, IRCoT, FLARE, GraphRAG, HippoRAG, RAPTOR | [03](03-classic-advanced-rag.md) |
| 4 | Learned retrieval policies | 18 / 14 | Search-R1 → UR² → AutoSearch; QuCo-RAG; SPARKLE; RAG-on-a-Diet; Retrieval Bottleneck | [04](04-learned-retrieval-policies.md) |
| 5 | Latent retrieval | 6 / 4 | LatentRAG (CLaRa for contrast) | [05](05-latent-retrieval.md) |
| 6 | Memory and state | 8 / 5 | State-Aware RAG, QueryLink, EgoMemory | [06](06-memory-and-state.md) |
| 7 | Knowledge representation | 8 / 5 | T²RAG, HiKEY, HiGoE | [07](07-knowledge-representation.md) |
| 8 | Evidence and trust | 8 / 3 | FRANQ, conflicts, poisoning | [08](08-evidence-and-trust.md) |
| 9 | Multimodal | 8 / 4 | Chart-MRAG, CMC-Bench, ColPali, HiKEY | [09](09-multimodal-rag.md) |
| 10 | Efficiency | 5 / 2 | SpecCache, RAGCache/CacheBlend, LatentRAG, AutoSearch | [10](10-efficiency.md) |
| 11 | Evaluation | 4 / 0* | CRAG, FRAMES, MultiHop-RAG; why numbers don't compare | [11](11-evaluation.md) |
| 12 | Open problems | 5 / 3 | the research gaps | [12](12-open-problems.md) |
| 13 | Recap and references | 2 / 1 | three takeaways | — |

**Optional modules** for a longer course or a second session (about 45 minutes each):

| Module | Content | Docs |
|---|---|---|
| Deep research agents | architectures, open training recipes (WebSailor, OpenResearcher), BrowseComp-Plus, rubric/process evaluation | [13](13-deep-research.md) |
| RAG security | PoisonedRAG → InceptionRAG, prompt injection, KV-cache side channels, SLOT taxonomy, defenses | [15](15-security.md) |
| RAG in production | defaults, symptom → fix table, infrastructure, evaluation loop | [17](17-production-guide.md) |
| Long context vs RAG | Self-Route, OP-RAG, LongRAG, LaRA; context engineering | [14](14-long-context-vs-rag.md) |
| Domain RAG | MIRAGE, Legal RAG Bench, FinanceBench, CRAG-MM | [16](16-domain-and-enterprise-rag.md) |

\* In the 90-minute version, fold the "numbers don't compare" slide into Section 4.

## Deep-dive template (4–5 slides per paper, the same pattern as the KDD 2026 tutorial)
1. **Problem and gap**: what failed before, with one piece of evidence.
2. **Key idea**: one diagram.
3. **Method**: components and training.
4. **Results and limitations**: one headline number on the slide; the full table goes in the appendix.
5. **What changed**: one sentence answering "what can this do that the previous approach couldn't?"

**Deep-dives** (one canonical method per idea): Search-R1, UR², AutoSearch, QuCo-RAG, LatentRAG, State-Aware RAG, T²RAG, HiKEY.
**One-slide mentions:** SPARKLE, RAG-on-a-Diet, The Retrieval Bottleneck, HiPRAG, Agentic-R, BrowseComp-Plus, HiGoE, TH-RAG, ParallaxRAG, MegaRAG, FRANQ, Chart-MRAG, CMC-Bench, InceptionRAG, SpecCache, QueryLink, EgoMemory.

**Ready-made deck:** [`slides/advanced-rag.md`](../slides/advanced-rag.md) (47 Marp slides with speaker notes, polls and demo cues).

## Status labels on every paper slide
`ACL 2026 main` · `Findings ACL 2026` · `Workshop` · `arXiv`. The status of each paper is in [papers/README.md](../papers/README.md).

## Audience interaction (one every ~15 minutes)
1. (§1) *"BM25 or dense for a query about a rare drug name?"*
2. (§2) Show the naive-RAG retrieval for the running example. *"What's missing?"*
3. (§3) *"Who decided every CoT sentence should trigger a search?"* (IRCoT)
4. (§4) *"You have one month to raise 70% accuracy: RL policy, better retrieval, or bigger LLM?"*
5. (§5) *"Would you ship latent queries in a bank?"*
6. (§8) Show a true-but-unsupported claim. *"Hallucination or not?"* (FRANQ)
7. (§11) Show two papers' HotpotQA numbers side by side. *"Which method is better?"* (Trick question.)

## Three takeaways (closing slide)
1. **Retrieval decisions are becoming learned:** when (UR², QuCo-RAG), what (T²RAG, LatentRAG), how much (AutoSearch).
2. **Retrieval quality is still the ceiling:** fix corpus, parsing and retriever before tuning RL (Retrieval Bottleneck; State-Aware RAG's +22.2% from Google Search; HiKEY).
3. **Trust and cost are now first-class research objectives,** not afterthoughts (FRANQ, SpecCache, AutoSearch, RAG-on-a-Diet).

## Production checklist
- [ ] Speaker notes for every slide; mark the slides to cut in the 90-minute version.
- [ ] Backup slides: GRPO vs PPO; how EM is computed; GraphRAG's cost; a latency breakdown.
- [ ] Every number on a slide is traceable to a paper page (see [verification-log.md](verification-log.md)).
- [ ] Re-check arXiv and the ACL Anthology the week before, and update the "as of" date.
- [ ] Send the [reading list](reading-list.md) one week ahead.

## Existing material to build on (credit it and ask before reusing slides)
- **KDD 2026 tutorial**, *RAG: From Modular to Agentic Systems* (Dong, Sharma, Yih, Xia, Yang, Sun, Wang, Zhang; Meta/UW), 3.5 h: [page](https://tutorial.lunadong.com/) · [slides PDF](https://tutorial.lunadong.com/slides.pdf) · [paper](https://tutorial.lunadong.com/paper.pdf) · [paper DB (about 2,000 papers)](https://papers.lunadong.com). The page shows no license.
- **ACL 2023 tutorial**, *Retrieval-based Language Models and Applications* (Asai, Min, Zhong, Chen): [site](https://acl2023-retrieval-lm.github.io/). Good for foundations.
- **DeepLearning.AI RAG course** lecture notes: [link](https://community.deeplearning.ai/t/rag-lecture-notes/852809). Practitioner basics.

None of these covers LatentRAG, State-Aware RAG, AutoSearch, T²RAG, HiKEY or the other 2026 papers. That part is original.
