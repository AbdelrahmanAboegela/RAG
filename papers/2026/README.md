# 2026 catalogue

The [paper index](../README.md) lists the 2026 papers with full notes. This page adds **more 2026 work, mostly arXiv preprints**, grouped by topic, with one paragraph each. Every entry was written from the paper's arXiv abstract (retrieved September 29, 2026). Treat preprints as preprints: label them `arXiv` on slides, and read the paper before quoting a number.

Status: ⬜ arXiv · 🟦 ACL 2026 main · 🟩 Findings · 🔷 other venue (named)

## Agentic search and RL training

| Paper | Status | What it does |
|---|---|---|
| **CIPO**, *Contextual Information Policy Optimization for Search Agents* · [2608.06128](https://arxiv.org/abs/2608.06128) | ⬜ | Diagnoses **prior-driven reasoning**: agents decide from internal knowledge and use search only to confirm, which is confirmation bias. CIPO gives dense, turn-level credit to reasoning actions that are actually *influenced by* retrieved evidence, combined with the outcome reward. It needs no process annotations and no reward model. |
| **AgenticRag-R1** · [2608.29622](https://arxiv.org/abs/2608.29622) | ⬜ | RL with a **memory stack** and a fine-grained action space (reason / retrieve / memorise), hierarchical action-aware rewards, and information-aware trajectory rejection for long-horizon learning. It attacks the "coarse actions + trajectory-level reward → short, stereotyped templates" failure. |
| **Critic-R** · [2606.00590](https://arxiv.org/abs/2606.00590) | ⬜ | A critic reads the agent's reasoning after each retrieval and judges whether the evidence supports the next step. *Critic-R-Zero* rewrites queries and retrieval instructions at inference time. *Critic-Embed* trains the retriever from successful and failed refinement trajectories, with no relevance labels. Evaluated on HotpotQA, 2Wiki, MuSiQue and Bamboogle. |
| **Return or Revise?** · [2609.30087](https://arxiv.org/abs/2609.30087) | ⬜ | When should you revise a draft answer with retrieved evidence? The paper trains a policy to predict the *paired effect* of revising ("recoverability") rather than draft correctness. It closes more than a third of the oracle gap over always revising, but still applies 38–46% of harmful revisions. Choosing between the draft and a plain-RAG answer is stronger still. |
| **Retrieval-Augmented LLM Agents: Learning to Learn from Experience** · [2603.18272](https://arxiv.org/abs/2603.18272) | 🔷 EMNLP 2026 (per arXiv) | Retrieves past **trajectories** (episodic memory) and integrates experience retrieval into LoRA fine-tuning. This substantially improves generalisation to unseen tasks, even when the retrieved experience is imperfect. |

## Deep research

| Paper | Status | What it does |
|---|---|---|
| **OpenResearcher** · [2603.20278](https://arxiv.org/abs/2603.20278) | ⬜ | Offline 15M-document environment and 97K synthesised long-horizon trajectories. A 30B-A3B model reaches 54.8% on BrowseComp-Plus. [Note](openresearcher.md) |
| **DeepResearch-9K** · [2603.01152](https://arxiv.org/abs/2603.01152) | ⬜ | 9,000 questions at three difficulty levels with trajectories from Tongyi-DeepResearch-30B-A3B, plus an open RL framework (**DeepResearch-R1**) supporting rule-based and LLM-judge rewards. 💻 [Applied-Machine-Learning-Lab/DeepResearch-R1](https://github.com/Applied-Machine-Learning-Lab/DeepResearch-R1) |
| **MMDeepResearch-Bench** · [2601.12346](https://arxiv.org/abs/2601.12346) | ⬜ | 140 expert tasks across 21 domains with image–text bundles. It evaluates report quality, citation alignment and text–visual integrity separately, across 25 models. Finding: strong prose ≠ faithful evidence use. |
| **MiroEval** · [2603.28407](https://arxiv.org/abs/2603.28407) | ⬜ | 100 real-user tasks (30 multimodal), refreshable. Evaluates synthesis quality, **agentic factuality verification**, and the **research process** itself. Process quality predicts the outcome, and multimodal tasks cost systems 3–10 points. 💻 [MiroMindAI/MiroEval](https://github.com/MiroMindAI/MiroEval) |

## Graph and structured RAG

| Paper | Status | What it does |
|---|---|---|
| **TH-RAG** | 🟦 | Topic → subtopic → triplet hierarchy fixes fragmented LLM-built KGs. [Note](th-rag.md) |
| **ParallaxRAG** | 🟦 | Head-specific, multi-view KG retrieval motivated by attention-head specialisation. [Note](parallaxrag.md) |
| **MegaRAG** | 🟦 | Multimodal KG construction, retrieval and generation. [Note](megarag.md) |
| **ConRAG** · [2605.28093](https://arxiv.org/abs/2605.28093) | ⬜ | Optimises both the query side (decomposition) and the corpus side (an evidence-grounded KG), and retrieves by **consensus across relation, entity and text views**. Up to +26.9% average over vanilla RAG on three multi-hop benchmarks. |
| **PAGE-RAG** · [2608.29753](https://arxiv.org/abs/2608.29753) | ⬜ | Builds a **temporary query-local graph** over retrieved candidates and treats each edge as a *support hypothesis*, not as support. This addresses the "connectivity–support gap". Paths are scored with provenance, specificity, hubness and coherence signals. Plug-in: +10.4 support F1 and +3.3 answer F1 at a fixed budget. |
| **Co-E**, *Co-Evolving Graph and Text Memory* · [2607.23278](https://arxiv.org/abs/2607.23278) | ⬜ | Training-free. Keeps a **synchronised graph memory and text memory** during reasoning: consolidate the text, extract triples into the graph, inject graph facts back. Same first author as State-Aware RAG. |
| **MG²-RAG** · [2604.04969](https://arxiv.org/abs/2604.04969) | ⬜ | A multi-granularity multimodal KG (text entities fused with visual regions). Graph construction is 43.3× faster and 23.9× cheaper than advanced graph-based frameworks. |

## Retrievers for reasoning and agents

| Paper | Status | What it does |
|---|---|---|
| **Agentic-R** | 🟩 | Retriever trained on local relevance + global answer correctness, co-optimised with the agent. [Note](agentic-r.md) |
| **RGLT**, *Retrieval Grounding Latent Reasoning for Dense Retrieval* · [2608.14107](https://arxiv.org/abs/2608.14107) | ⬜ | A dense retriever that "thinks" in latent "silent tokens" before embedding. Each latent step is supervised to *increase* retrieval quality, to stop shortcut reasoning. |
| **EvoEmbedding** · [2606.21649](https://arxiv.org/abs/2606.21649) | ⬜ | **Evolvable embeddings**: the encoder keeps a latent memory while reading a long context sequentially, so the same query retrieves different targets as the context evolves. A naive RAG pipeline using it beats dedicated agentic-memory systems. |
| **CoRM-RAG** · [2605.01302](https://arxiv.org/abs/2605.01302) | ⬜ | The **relevance–robustness gap**: for queries with false premises or confirmation bias, the most *relevant* evidence is often *sycophantic*. An evidence critic trained with simulated cognitive biases ranks documents by whether they can steer the model to the right answer. 💻 [PeiYangLiu/CoRM-RAG](https://github.com/PeiYangLiu/CoRM-RAG) |

## Interpretability and failure analysis

| Paper | Status | What it does |
|---|---|---|
| **Why RAG Fails: A Graph Perspective** · [2605.14192](https://arxiv.org/abs/2605.14192) | ⬜ | Circuit tracing and **attribution graphs** of how retrieved evidence flows through layers. Correct answers show deeper, more distributed evidence flow; failures are shallow and concentrated. Topology features detect errors, and targeted interventions reduce them. |
| **Chain of Evidence (CoE)** · [2605.01284](https://arxiv.org/abs/2605.01284) | ⬜ | **Pixel-level attribution** for iterative RAG: a VLM reasons over *screenshots* of retrieved pages and outputs bounding boxes for each evidence step (Wiki-CoE, SlideVQA). 💻 [PeiYangLiu/CoE](https://github.com/PeiYangLiu/CoE) |

## Multimodal agentic search

| Paper | Status | What it does |
|---|---|---|
| **SimpleSearch-VL** · [2606.31504](https://arxiv.org/abs/2606.31504) | ⬜ | Multimodal agentic search from 5K SFT trajectories + 2K RL examples. Factorized Adaptive Rollout improves sampling efficiency, and chain-of-thought verification checks evidence. +15.8 / +16.0 points over Qwen3-VL agentic baselines (8B / 30B-A3B). |

## Serving, caching and efficiency

| Paper | Status | What it does |
|---|---|---|
| **PCR** · [2603.23049](https://arxiv.org/abs/2603.23049) | ⬜ | KV-cache reuse *system*: prefix tree with look-ahead LRU, layer-wise overlap of KV loading with compute, and SSD→DRAM prefetching from the scheduler queue. Up to 2.47× faster average TTFT. |
| **GroundedCache** · [2605.27494](https://arxiv.org/abs/2605.27494) | ⬜ | *When* is reusing a cached **answer** safe? Four gates: query similarity, evidence overlap, source version, and lexical support in fresh evidence. The unsafe-served rate falls from 15–35% to 0% on HotpotQA regimes. 💻 [syedhumarahim/grounded-cache-router](https://github.com/syedhumarahim/grounded-cache-router) · toy version: [`code/ragkit/cache.py`](../../code/ragkit/cache.py) |
| **FinCacheServe** · [2607.26076](https://arxiv.org/abs/2607.26076) | ⬜ | Answer reuse over **mutable enterprise documents** (SEC filings), keyed by document versions, evidence and tool fingerprints, model and decoding config. Skips about 53% of LLM calls with zero observed stale outputs. |

## Security

| Paper | Status | What it does |
|---|---|---|
| **InceptionRAG** | 🔷 CCS 2026 | Poisoning split across harmless-looking passages that the LLM chains into misinformation. [Note](inceptionrag.md) |
| **Securing RAG: A Taxonomy (SLOT)** · [2604.08304](https://arxiv.org/abs/2604.08304) | ⬜ | Survey. The **SLOT** taxonomy covers attack **S**urface, defense **L**ayer, **O**bjective (CIA triad) and **T**arget, mapped onto a six-stage knowledge-access pipeline. 💻 [TreeAI-Lab/Awesome-RAG-Security](https://github.com/TreeAI-Lab/Awesome-RAG-Security) |
| **TRACE** (poisoning detection) · [2606.25721](https://arxiv.org/abs/2606.25721) | 🔷 EMNLP 2026 Industry (per arXiv) | Lightweight detection by **token-influence attribution**: finds recurring high-influence keywords across retrieved documents and recovers the attacker's target answer. Not to be confused with MMDR-Bench's TRACE citation metric. |
| **SpliceLeak** · [2606.21842](https://arxiv.org/abs/2606.21842) | ⬜ | Timing side channel on **non-prefix KV-cache fusion** (vLLM + LMCache): leaks the length and then the content of other users' private prompts. The proposed defense, SpliceDefense, pads chunks and uses constant-time fusion. |

## Domain RAG

| Paper | Status | What it does |
|---|---|---|
| **Legal RAG Bench** · [2603.01710](https://arxiv.org/abs/2603.01710) | ⬜ | 4,876 passages (Victorian Criminal Charge Book) and 100 expert questions, in a full-factorial design. **Retrieval is the primary driver**: the best embedder added +17.5 correctness and +34 retrieval accuracy. Many "hallucinations" were retrieval failures. |
| **AgenticRAG** (enterprise) · [2605.05538](https://arxiv.org/abs/2605.05538) | ⬜ | Gives a reasoning LLM **search / find / open / summarize** tools over existing enterprise search. BRIGHT recall@1 is 49.6% (+21.8 pp), and FinanceBench correctness is 92%, within 2 pp of oracle evidence. The shift from single-shot to agentic tool use was the largest factor (5.9×). |
| **Goal-Mem** · [2605.12213](https://arxiv.org/abs/2605.12213) | ⬜ | Conversational agent memory by **backward chaining** from the user's goal into sub-goals, each resolved by targeted memory retrieval, formalised as "Natural Language Logic". |
