# Advanced RAG: Papers, Explanations, Code and Current Trends

> **From a pipeline you engineer to a policy the model learns.**
> A curated, **verified** collection of papers, code and explanations on advanced Retrieval-Augmented Generation (RAG), with a focus on the 2025–2026 frontier: RL-trained search agents, latent retrieval, memory, structured knowledge, multimodal RAG, trust and efficiency.

*Last verified: **29 September 2026*** · venues and numbers checked against ACL Anthology and arXiv pages; see the [verification log](docs/verification-log.md).

---

## What's in this repo

```
.
├── docs/            13-chapter course on advanced RAG + lecture outline + reading list + verification log
├── papers/          one note per key paper: problem → idea → method → results → limitations → what changed
│   ├── 2026/        17 papers from ACL 2026 (main + Findings), arXiv and workshops
│   ├── 2025/        Search-R1 in depth + a catalogue of the 2025 RL-for-search wave
│   └── foundations/ the 2020–2024 papers everything else assumes
├── code/            dependency-free reference implementations (BM25, RRF, Search-R1 loop,
│                    AutoSearch reward, QuCo-RAG triggers, T²RAG loop) + tests + runnable examples
└── experiments/     how to run each paper's OFFICIAL code (commands copied from each repo's README)
```

| If you want to… | Start here |
|---|---|
| Understand the field in 20 minutes | [docs/00-overview.md](docs/00-overview.md) |
| Learn RAG properly, start to finish | [docs/](docs/README.md), chapters 01 → 12 |
| Catch up on 2026 | [papers/README.md](papers/README.md) and [docs/04](docs/04-learned-retrieval-policies.md) |
| See the mechanisms in code | [code/](code/README.md) (`python -m unittest discover -s code/tests`) |
| Reproduce a paper | [experiments/](experiments/README.md) |
| Teach a lecture on it | [docs/lecture-outline.md](docs/lecture-outline.md) |

---

## The thesis in one table

| Decision | Pipeline era (2020) | "Advanced RAG" (2023–24) | Learned policy (2025–26) |
|---|---|---|---|
| **When** to retrieve | always, once | uncertainty thresholds (FLARE, DRAGIN); reflection tokens (Self-RAG) | RL policy (Search-R1); difficulty-aware (**UR²**); corpus statistics (**QuCo-RAG**) |
| **What** to retrieve | the question | rewriting, HyDE, decomposition (IRCoT) | learned sub-queries; placeholder triplets (**T²RAG**); document trees (**HiKEY**); latent vectors (**LatentRAG**) |
| **How much** | fixed top-k | reranking, compression | learned stopping depth (**AutoSearch**); cost per hop (**RAG-on-a-Diet**) |
| **How to use** it | concatenate | Chain-of-Note, CRAG | trained working memory (**State-Aware RAG**); plug-and-play proxies (**SPARKLE**) |
| **At what cost** | ignored | prefix caching | latent reasoning (**LatentRAG**); speculative KV repair (**SpecCache**) |

**Caveat that governs everything:** retrieval quality still sets the ceiling (**The Retrieval Bottleneck**, ACL 2026).

---

## 2026 papers

Status: 🟦 **ACL 2026 main** · 🟩 **Findings of ACL 2026** · 🟨 workshop · ⬜ arXiv preprint · 💻 = code available

### Learned retrieval policies (when / whether / how much to retrieve)
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **UR²**: Unify RAG and Reasoning through RL | 🟦 | difficulty-aware curriculum (retrieve only when hard) + LLM-summarised evidence + two-stage RL | 3B–8B models ≈ GPT-4o-mini / GPT-4.1-mini on several benchmarks | [note](papers/2026/ur2.md) · [paper](https://aclanthology.org/2026.acl-long.580/) · [💻](https://github.com/Tsinghua-dhy/UR2) |
| **AutoSearch**: Adaptive Search Depth via RL | 🟩 | self-answer after each search; reward stopping at the minimal sufficient depth | 7B: 48.0 EM at depth 1.27 vs StepSearch 40.0 at 2.08 | [note](papers/2026/autosearch.md) · [paper](https://aclanthology.org/2026.findings-acl.1399/) · [💻](https://github.com/bofusun/AutoSearch) |
| **QuCo-RAG**: Uncertainty from the Pre-training Corpus | 🟩 | retrieve when entities are rare, or never co-occur, in the pre-training data (Infini-gram) | +5–12 EM over FLARE/DRAGIN/SeaKR on OLMo-2; training-free | [note](papers/2026/quco-rag.md) · [arXiv](https://arxiv.org/abs/2512.19134) · [💻](https://github.com/ZhishanQ/QuCo-RAG) |
| **SPARKLE**: Plug-and-play Agentic Retrieval Policy | 🟦 | a 3B PPO-trained proxy controls retrieval for a frozen LLM, via KG-style triplet chains | +9.17% in-domain / +2.85% out-of-domain average | [note](papers/2026/sparkle.md) · [paper](https://aclanthology.org/2026.acl-long.1793/) · [💻](https://github.com/jyfang6/sparkle) |
| **RAG-on-a-Diet** | 🟦 | an RL agent picks the model size (4B / 30B / 671B) per hop | −60% cost vs IRCoT for −3.7 F1 on HotpotQA | [note](papers/2026/rag-on-a-diet.md) · [paper](https://aclanthology.org/2026.acl-long.1562/) |
| **The Retrieval Bottleneck**: Scaling Laws for RL in RAG | 🟦 | sigmoidal RL scaling; the ceiling is set by retrieval quality | 3.1% extrapolation error at 4× compute | [note](papers/2026/retrieval-bottleneck.md) · [paper](https://aclanthology.org/2026.acl-long.1478/) |

### Latent retrieval
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **LatentRAG**: Latent Reasoning and Retrieval for Efficient Agentic RAG | ⬜ | thoughts and sub-queries as latent tokens in one forward pass, aligned to the dense retriever | Search-R1-level EM at **about 90% lower latency** (593 ms vs 5,372 ms) | [note](papers/2026/latentrag.md) · [arXiv](https://arxiv.org/abs/2605.06285) |

### Memory and state
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **State-Aware RAG** ("Reasoning with Memory") | 🟩 | a trained 4B extractor curates working memory each hop; Path-Outcome Dual Reward (GRPO) | +8.6% vs HippoRAG 2; +9.3% vs s3 | [note](papers/2026/state-aware-rag.md) · [paper](https://aclanthology.org/2026.findings-acl.1834/) · [💻](https://github.com/amazon-science/state-aware-rag) |
| **QueryLink** | 🟩 | multi-view query–memory alignment + coherent memory chunking | ≥7% on LoCoMo / LongMemEval | [note](papers/2026/querylink.md) · [paper](https://aclanthology.org/2026.findings-acl.765/) · [💻](https://github.com/Dontplay0112/querylink) |
| **EgoMemory** | 🟩 | personalised retrieval over egocentric video; training-free MLLM + reflective CoT | new benchmark: 245 videos, 45 people, 639 queries | [note](papers/2026/egomemory.md) · [paper](https://aclanthology.org/2026.findings-acl.362/) |

### Knowledge representation
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **T²RAG**: Beyond Chunks and Graphs | 🟩 | graph-free triplet index; question → placeholder triplets resolved iteratively | up to +11% average; −45% retrieval cost | [note](papers/2026/t2rag.md) · [paper](https://aclanthology.org/2026.findings-acl.1310/) · [💻](https://github.com/Emory-Melody/T2RAG) |
| **HiKEY**: Hierarchical Multimodal Retrieval for Document QA | 🟦 | parse the document tree; route document → section → unit; budgeted evidence packing | up to +12.9% recall, +6.8% QA | [note](papers/2026/hikey.md) · [arXiv](https://arxiv.org/abs/2605.29606) |
| **HiGoE**: Hierarchical Graph of Evidence | 🟦 | proposition–evidence graph + PPR + GAT for long-context **summarization** | beats baselines in quality and efficiency | [note](papers/2026/higoe.md) · [paper](https://aclanthology.org/2026.acl-long.902/) · [💻](https://github.com/tkw123/HiGOE) |

### Evidence, trust and multimodal
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **FRANQ** | 🟩 | hallucination detection that separates factuality from faithfulness to context | better factual-error detection than UQ and hallucination baselines | [note](papers/2026/franq.md) · [paper](https://aclanthology.org/2026.findings-acl.338/) |
| **Chart-MRAG** | 🟦 | chart-based multimodal RAG benchmark (4,738 QA, 8 domains) | best MLLMs: 71.15% correctness even with gold retrieval | [note](papers/2026/chart-mrag.md) · [paper](https://aclanthology.org/2026.acl-long.1164/) · [💻](https://github.com/Nomothings/CHARGE) |
| **CMC-Bench** ("When Image and Text Disagree") | 🟨 | cross-modal evidence conflicts | VLMs abstain (31.7%) or fabricate (51.9%) | [note](papers/2026/cmc-bench.md) · [paper](https://aclanthology.org/2026.magmar-main.3/) |

### Efficiency
| Paper | Status | One-line idea | Headline result | Links |
|---|---|---|---|---|
| **SpecCache** | 🟦 | a small model's hidden-state norms choose which reused-KV tokens to recompute | TTFT 2.17–3.95× faster; throughput 2.7–5.2× | [note](papers/2026/speccache.md) · [paper](https://aclanthology.org/2026.acl-long.859/) |

### Surveys and tutorials (2026)
- **KDD 2026 tutorial**, *RAG: From Modular to Agentic Systems* (Dong et al., Meta/UW): [page](https://tutorial.lunadong.com/) · [slides](https://tutorial.lunadong.com/slides.pdf) · [paper](https://tutorial.lunadong.com/paper.pdf) · [2,000-paper DB](https://papers.lunadong.com)
- **SoK: Agentic RAG**: taxonomy, architectures, evaluation (March 2026): [arXiv:2603.07379](https://arxiv.org/abs/2603.07379)
- **Scaling Beyond Context**: a survey of multimodal RAG for document understanding (ACL 2026): [paper](https://aclanthology.org/2026.acl-long.204/)

---

## 2025: the RL-for-search turn

| System | Idea | Links |
|---|---|---|
| **Search-R1** ⭐ | outcome-reward RL with interleaved `<search>`; masks retrieved tokens | [note](papers/2025/search-r1.md) · [arXiv](https://arxiv.org/abs/2503.09516) · [💻](https://github.com/PeterGriffinJin/Search-R1) |
| Search-o1 | a reasoning model searches mid-thought; Reason-in-Documents | [arXiv](https://arxiv.org/abs/2501.05366) · [💻](https://github.com/sunnynexus/Search-o1) |
| R1-Searcher | two-stage RL: retrieval format, then correctness | [arXiv](https://arxiv.org/abs/2503.05592) · [💻](https://github.com/RUCAIBox/R1-Searcher) |
| ReSearch | search as part of the reasoning chain; GRPO | [arXiv](https://arxiv.org/abs/2503.19470) · [💻](https://github.com/Agent-RL/ReSearch) |
| DeepResearcher | RL in the real web environment | [arXiv](https://arxiv.org/abs/2504.03160) · [💻](https://github.com/GAIR-NLP/DeepResearcher) |
| WebThinker | deep-research agent that drafts reports while thinking | [arXiv](https://arxiv.org/abs/2504.21776) · [💻](https://github.com/RUC-NLPIR/WebThinker) |
| ZeroSearch | an LLM simulates the search engine during RL | [arXiv](https://arxiv.org/abs/2505.04588) · [💻](https://github.com/Alibaba-NLP/ZeroSearch) |
| s3 | train only the searcher; "Gain Beyond RAG" reward | [arXiv](https://arxiv.org/abs/2505.14146) · [💻](https://github.com/pat-jj/s3) |
| CLaRa (Apple) | retrieval and generation in a shared continuous space | [arXiv](https://arxiv.org/abs/2511.18659) · [💻](https://github.com/apple/ml-clara) |

More in [papers/2025/README.md](papers/2025/README.md).

---

## Foundations (2020–2024)

**Retrieval-augmented LMs:** [RAG](https://arxiv.org/abs/2005.11401) · [REALM](https://arxiv.org/abs/2002.08909) · [FiD](https://arxiv.org/abs/2007.01282) · [RETRO](https://arxiv.org/abs/2112.04426) · [Atlas](https://arxiv.org/abs/2208.03299)
**Retrievers:** [DPR](https://arxiv.org/abs/2004.04906) · [ColBERT](https://arxiv.org/abs/2004.12832) · [SPLADE](https://arxiv.org/abs/2107.05720) · [Contriever](https://arxiv.org/abs/2112.09118) · [E5](https://arxiv.org/abs/2212.03533) · [HyDE](https://arxiv.org/abs/2212.10496)
**Failure modes:** [Lost in the Middle](https://arxiv.org/abs/2307.03172) · [Irrelevant context](https://arxiv.org/abs/2310.01558) · [ClashEval](https://arxiv.org/abs/2404.10198) · [Knowledge conflicts survey](https://arxiv.org/abs/2403.08319) · [PoisonedRAG](https://arxiv.org/abs/2402.07867)
**Advanced RAG toolkit:** [Self-Ask](https://arxiv.org/abs/2210.03350) · [IRCoT](https://arxiv.org/abs/2212.10509) · [FLARE](https://arxiv.org/abs/2305.06983) · [DRAGIN](https://arxiv.org/abs/2403.10081) · [Self-RAG](https://arxiv.org/abs/2310.11511) · [CRAG](https://arxiv.org/abs/2401.15884) · [Adaptive-RAG](https://arxiv.org/abs/2403.14403) · [RECOMP](https://arxiv.org/abs/2310.04408) · [Chain-of-Note](https://arxiv.org/abs/2311.09210) · [Speculative RAG](https://arxiv.org/abs/2407.08223) · [RankRAG](https://arxiv.org/abs/2407.02485)
**Structured knowledge:** [GraphRAG](https://arxiv.org/abs/2404.16130) · [HippoRAG](https://arxiv.org/abs/2405.14831) / [HippoRAG 2](https://arxiv.org/abs/2502.14802) · [LightRAG](https://arxiv.org/abs/2410.05779) · [RAPTOR](https://arxiv.org/abs/2401.18059)
**Multimodal:** [ColPali](https://arxiv.org/abs/2407.01449) · [VisRAG](https://arxiv.org/abs/2410.10594)
**Efficiency:** [RAGCache](https://arxiv.org/abs/2404.12457) · [CacheBlend](https://arxiv.org/abs/2405.16444)
**Evaluation:** [CRAG benchmark](https://arxiv.org/abs/2406.04744) · [FRAMES](https://arxiv.org/abs/2409.12941) · [MultiHop-RAG](https://arxiv.org/abs/2401.15391) · [BRIGHT](https://arxiv.org/abs/2407.12883) · [RAGAS](https://arxiv.org/abs/2309.15217) · [ARES](https://arxiv.org/abs/2311.09476) · [ALCE](https://arxiv.org/abs/2305.14627)
**Surveys:** [Gao et al. 2023/24](https://arxiv.org/abs/2312.10997) · [RAG-Reasoning survey 2025](https://arxiv.org/abs/2507.09477) · [Agentic RAG survey 2025](https://arxiv.org/abs/2501.09136)

Each of these has a what/how/why entry in [papers/foundations/README.md](papers/foundations/README.md).

---

## Code

```bash
python -m unittest discover -s code/tests      # 17 tests, standard library only
python code/examples/01_hybrid_retrieval.py    # naive RAG fails on a 4-hop question
python code/examples/02_agentic_loop.py        # Search-R1 protocol + AutoSearch reward
python code/examples/03_quco_trigger.py        # QuCo-RAG's corpus-statistics triggers
python code/examples/04_t2rag.py               # T²RAG solves it in 2 rounds
```

The examples share one running question: *"Are the directors of Move (1970) and Méditerranée (1963) from the same country?"* See [code/README.md](code/README.md).

## Tools and frameworks

[FlashRAG](https://github.com/RUC-NLPIR/FlashRAG) · [UltraRAG](https://github.com/OpenBMB/UltraRAG) · [LlamaIndex](https://github.com/run-llama/llama_index) · [LangGraph](https://github.com/langchain-ai/langgraph) · [Haystack](https://github.com/deepset-ai/haystack) · [RAGFlow](https://github.com/infiniflow/ragflow) · [GraphRAG](https://github.com/microsoft/graphrag) · [LightRAG](https://github.com/HKUDS/LightRAG) · [HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) · [ColPali](https://github.com/illuin-tech/colpali) · [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) · [verl](https://github.com/volcengine/verl) · [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) · [vLLM](https://github.com/vllm-project/vllm) · [LMCache](https://github.com/LMCache/LMCache) · [RAGAS](https://github.com/explodinggradients/ragas) · [Mem0](https://github.com/mem0ai/mem0) · [A-MEM](https://github.com/agiresearch/A-mem) · [STORM](https://github.com/stanford-oval/storm)

## Other awesome lists
[Awesome-RAG-Reasoning](https://github.com/DavidZWZ/Awesome-RAG-Reasoning) · [Awesome-RL-based-Agentic-Search-Papers](https://github.com/ventr1c/Awesome-RL-based-Agentic-Search-Papers) · [Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG) · [RAG-Survey](https://github.com/Tongji-KGLLM/RAG-Survey)

---

## How this repo stays honest

1. **Every paper has a status label**: ACL main, Findings, workshop or arXiv.
2. **Every paper note has a "Verified" row** saying what was read (abstract, full text or code) and when.
3. **Numbers are quoted only from the paper**, with the table or abstract they come from. Where sources disagree (Chart-MRAG), both are shown and the camera-ready figure is preferred.
4. **Numbers are not compared across papers.** See [docs/11](docs/11-evaluation.md#112-why-you-cant-compare-numbers-across-papers).
5. **Unverifiable items are excluded** and listed in the [verification log](docs/verification-log.md).

Contributions welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
