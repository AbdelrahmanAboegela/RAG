---
marp: true
theme: default
paginate: true
title: "Advanced RAG: from pipelines to learned policies"
description: Lecture deck. As of September 2026.
---

<!-- _class: lead -->
# Advanced RAG
## From a pipeline you engineer to a policy the model learns

*As of September 2026*

<!-- Speaker notes: Introduce yourself. Promise: one thesis, four questions, one running example. Everything on the slides has a status label (ACL main / Findings / workshop / arXiv). -->

---

## Why this lecture
- LLMs hallucinate on long-tail facts and go stale
- RAG grounds answers in retrieved evidence
- But "retrieve top-k, then read" breaks on hard questions
- 2025–26: retrieval decisions are increasingly **learned**

<!-- Notes: Ask: who has shipped a RAG system? Who was happy with it? -->

---

## Thesis and four questions

**RAG is shifting from a pipeline you engineer to a policy the model learns.**

1. **When** to retrieve?
2. **What** to retrieve, in which representation?
3. **How** to use what was retrieved?
4. **At what cost?**

<!-- Notes: Every paper today answers at least one of these. -->

---

## Running example

> *Are the directors of **Move** (1970) and **Méditerranée** (1963) from the same country?*

| Hop | Fact |
|---|---|
| 1 | Move (1970) → Stuart Rosenberg |
| 2 | Méditerranée (1963) → Jean-Daniel Pollet |
| 3 | Rosenberg → American |
| 4 | Pollet → French → **No** |

<!-- Notes: 2WikiMultihopQA style; also Figure 1 of the State-Aware RAG paper. Replace with a domain question if you have one. Code: code/examples/corpus.py -->

---

## Taxonomy (not "RAG 1.0 → 4.0")

- **Modular RAG**: swappable retrieve / rerank / compress / generate modules
- **Graph-enhanced RAG**: graphs, trees, triplets
- **Agentic RAG**: an agent plans and retrieves over many turns
- **Deep research**: long-horizon agents that write cited reports

<!-- Notes: "RAG 1.0–4.0" is an informal framing; the three-paradigm split is used by the KDD 2026 tutorial (Dong et al.) and the surveys. -->

---

<!-- _class: lead -->
# 1. Foundations

---

## The pipeline

`parse → chunk → embed/index` … `query → rewrite → retrieve → rerank → pack → generate`

- Each box changes results more than most model upgrades
- Parsing is where most production errors start

---

## Retrieval: sparse, dense, hybrid

| | Strength | Weakness |
|---|---|---|
| BM25 | rare entities, no training | vocabulary mismatch |
| Dense (E5, BGE, Qwen3-Emb) | paraphrase, semantics | rare names, prefixes |
| Late interaction (ColBERT) | accuracy | index size |
| **Hybrid + RRF** | robust default | two indexes |

`score(d) = Σ 1/(60 + rank(d))`

<!-- Poll: "BM25 or dense for a query about a rare drug name?" Answer: BM25 often wins; best is hybrid. -->

---

## Chunking and reranking

- 100-word passages: the research default (DPR)
- Structure-aware chunks + parent pointers: the production default
- **Retrieve 50–100 → rerank to 5–10** (cross-encoder or LLM)
- 2025: **reasoning rerankers** (Rank1) and **reasoning retrievers** (ReasonIR)

---

<!-- _class: lead -->
# 2. Why vanilla RAG fails

---

## Five failure modes

1. **Multi-hop**: the first query can't reach the answer
2. **Noise**: irrelevant passages push accuracy *below* no-retrieval
3. **Lost in the middle**: U-shaped use of context positions
4. **Conflicts**: context vs. memory, source vs. source, text vs. image
5. **Poisoning**: ~5 passages per target, ~90% attack success (PoisonedRAG)

<!-- Demo: python code/examples/01_hybrid_retrieval.py — no single query retrieves both nationality pages. Ask: "What's missing?" -->

---

<!-- _class: lead -->
# 3. The toolkit you need first

---

## Iterative and adaptive retrieval (2022–24)

| Method | When to retrieve | Learned? |
|---|---|---|
| IRCoT | every CoT sentence | prompted |
| FLARE / DRAGIN | low-confidence tokens | threshold |
| Self-RAG | `[Retrieve]` token | SFT (GPT-4 labels) |
| Adaptive-RAG | complexity classifier | SFT |

<!-- Poll: "Who decided every CoT sentence should trigger a search?" → leads into RL. -->

---

## Structure: graphs and trees

- **GraphRAG**: entity graph → communities → reports → map-reduce (global questions)
- **HippoRAG**: OpenIE KG + Personalized PageRank (multi-hop in one step)
- **RAPTOR**: recursive cluster summaries; retrieve across levels
- Shared cost: **LLM passes over the whole corpus**

<!-- Demo: python code/examples/05_graph_ppr.py — PPR reaches both nationality passages from the film seeds. -->

---

<!-- _class: lead -->
# 4. Learned retrieval policies

---

## Search-R1 (2025): the bridge

```
<think>…</think><search>q</search><information>docs</information>…<answer>a</answer>
reward = EM(a, gold)     # outcome only
mask retrieved tokens    # don't train on the retriever's text
PPO / GRPO, Qwen2.5-3B/7B, E5 over Wikipedia-2018
```

**What changed:** retrieval behaviour learned from the outcome, with no labels.

<!-- Demo: python code/examples/02_agentic_loop.py and 06_grpo.py. Point out that the 4-search and 5-search rollouts get the same advantage. -->

---

## UR² (ACL 2026 main): *whether* retrieval helps

- Problem: outside open QA, agents over-rely on retrieval or abandon it
- Difficulty-aware curriculum: retrieve only for **hard** items (from 20 rollouts)
- Hybrid knowledge: offline corpora + **LLM summaries**
- Two-stage RL: reward *using* retrieval, then correctness
- 3B–8B ≈ GPT-4o-mini / GPT-4.1-mini on several benchmarks

<!-- Limitation: summariser is an external LLM; its cost isn't counted. -->

---

## AutoSearch (Findings ACL 2026): *how much* to search

- Self-answer after every search
- **Minimal sufficient depth** t_c = first step with a correct intermediate answer
- Reward reaching t_c; penalise searching past it
- Qwen2.5-7B: **48.0 EM at depth 1.27** vs StepSearch 40.0 at 2.08

<!-- Limitation: needs exact-match intermediate answers → short-answer QA only. -->

---

## HiPRAG (ICLR 2026): per-decision process reward

- Was *this* search necessary? Was *this* non-search a mistake?
- Bonus for the fraction of optimal steps, on top of format + outcome
- Over-search rate **2.3%**; 65.4% / 67.2% average accuracy (3B / 7B)

---

## QuCo-RAG (Findings ACL 2026): ask the corpus, not the model

- Model confidence is poorly calibrated
- **Rare entity** in pre-training data (< 10³) → retrieve
- **Zero co-occurrence** of (head, tail) in generated claim → retrieve
- Infini-gram over OLMo-2's ~4T tokens, millisecond queries
- +5–12 EM over FLARE/DRAGIN/SeaKR; training-free

<!-- Demo: python code/examples/03_quco_trigger.py. Limitation (KDD tutorial): needs the pre-training corpus or a proxy. -->

---

## Who holds the policy? SPARKLE (ACL 2026 main)

- Train a **3B proxy** with PPO; LLM and retriever **frozen**
- Reasons over KG-style triplet chains to find gaps
- Transfers to other LLMs and retrievers without retraining
- +9.17% in-domain / +2.85% out-of-domain

---

## Cost-aware: RAG-on-a-Diet (ACL 2026 main)

- RL picks the **model size per hop** (4B / 30B / 671B)
- −60% cost vs IRCoT for −3.7 F1 on HotpotQA
- AutoSearch = fewer hops; Diet = cheaper hops

---

## The ceiling is retrieval

| Evidence | Effect |
|---|---|
| Retrieval Bottleneck (ACL 2026) | RL scaling asymptote set by retrieval quality |
| State-Aware RAG | Wikipedia → Google Search: **+22.2%** |
| BrowseComp-Plus (ACL 2026) | GPT-5: BM25 55.9% → Qwen3-Emb-8B **70.1%**, fewer searches |
| Legal RAG Bench | best embedder: +17.5 correctness |

<!-- Poll: "One month to raise 70% accuracy: RL policy, better retrieval, or bigger LLM?" -->

---

## Train the retriever for the agent

- **Agentic-R** (Findings 2026): local relevance + global answer correctness; agent ⇄ retriever co-optimised
- **R3** (2025): RL on the retriever
- **Critic-R** (2026): a critic judges whether evidence supports the next step

---

<!-- _class: lead -->
# 5. Latent retrieval

---

## LatentRAG (arXiv, May 2026)

- Search-R1 takes **16–22×** naive-RAG time; ~90% of it is decoding thoughts and queries
- 4 latent thought + 16 latent query tokens, **one forward pass**
- KL alignment to what the text query would retrieve
- 43.46 EM at **593 ms** vs Search-R1 42.47 at 5,372 ms (**−89%**)

<!-- Poll: "Would you ship latent queries in a bank?" Limitation: SFT-bounded; queries not auditable without the decoder. -->

---

<!-- _class: lead -->
# 6. Memory and state

---

## State-Aware RAG (Findings ACL 2026)

- Diagnosis: everyone optimises *acquisition*, nobody *management*
- Trained **4B extractor** curates working memory each hop
- Path-Outcome Dual Reward (GRPO); retriever and generator frozen
- +8.6% vs HippoRAG 2; +9.3% vs s3

<!-- Running example: memory after hop 4 = "Rosenberg: American; Pollet: French". -->

---

## Long-term memory

- **QueryLink** (Findings 2026): align queries and memories; ≥7% on LoCoMo / LongMemEval
- **EgoMemory** (Findings 2026): personalised egocentric-video retrieval
- Memory-R1, MemGPT/Letta, A-MEM, Mem0

---

<!-- _class: lead -->
# 7. Knowledge representation

---

## T²RAG (Findings ACL 2026): triplets, no graph

```
(Move (1970), directed by, ?d1)          searchable → round 1
(?d1, nationality, ?c1)                   fuzzy → searchable → round 2
```
- Graph-free triplet index + placeholder resolution
- Up to +11% average; −45% retrieval tokens vs IRCoT

<!-- Demo: python code/examples/04_t2rag.py -->

---

## HiKEY (ACL 2026 main): the document's own tree

- Parse the PDF hierarchy (LVLM); doc → section → unit routing
- Pack evidence with governing headers under a token budget
- FRAMES "All" +11.4; recall up to +12.9%, QA +6.8%
- The reader is now the bottleneck

---

## Graph RAG in 2026

- **TH-RAG**: topic hierarchy over triplets (ACL main)
- **ParallaxRAG**: head-specific multi-view KG retrieval (ACL main)
- **MegaRAG**: multimodal KGs (ACL main)
- **HiGoE**: evidence graphs for *summarization* (ACL main)
- Trend: cheaper graphs; graphs as temporary scaffolds

---

<!-- _class: lead -->
# 8. Evidence, trust and security

---

## Factuality ≠ faithfulness: FRANQ (Findings 2026)

| | faithful | unfaithful |
|---|---|---|
| **true** | ideal | *flagged as hallucination by most detectors* |
| **false** | bad source | hallucination |

<!-- Poll: show a true-but-unsupported claim. "Hallucination or not?" -->

---

## Attacks get smarter

- **PoisonedRAG**: one doc per payload
- **InceptionRAG** (CCS 2026): payload split across harmless passages; the LLM *reasons* its way to the lie. >80% ASR
- **SpliceLeak**: KV-cache timing leaks other users' prompts
- No complete defense exists

---

<!-- _class: lead -->
# 9. Multimodal

---

## Charts and conflicts

- **Chart-MRAG** (ACL 2026 main): even with gold retrieval, best MLLMs **71.15%** correctness; text-over-visual bias
- **CMC-Bench** (workshop): on image–text conflicts, VLMs abstain (31.7%) or fabricate (51.9%)
- ColPali / VisRAG / M3DocRAG: retrieve page images

---

<!-- _class: lead -->
# 10. Efficiency

---

## Four cost axes

| Axis | 2026 answer |
|---|---|
| number of steps | AutoSearch, HiPRAG |
| cost per step | RAG-on-a-Diet |
| decoding queries | LatentRAG |
| prefill of docs | **SpecCache** (TTFT 2.17–3.95×), CacheBlend, CacheClip |
| skip the LLM | safe answer caching (GroundedCache) |

---

<!-- _class: lead -->
# 11. Deep research

---

## From answers to reports

- Plan → search/open/find loop → verify → cited report
- Open recipes: WebSailor, WebDancer, **OpenResearcher** (offline 15M-doc env, 54.8% BrowseComp-Plus)
- Evaluation: BrowseComp-Plus, ResearchRubrics (<68% compliance), FINDER/DEFT, MiroEval
- Weak link: **evidence integration and verification**

---

<!-- _class: lead -->
# 12. Evaluation

---

## Don't compare numbers across papers

Same "HotpotQA", different:
- backbone (and Base vs Instruct)
- retriever and corpus
- top-k, max turns
- sample (full vs 1,000; Bamboogle = 125 questions)
- metric (EM / F1 / cover-EM / LLM-judge)

<!-- Demo: python code/examples/08_evaluate.py — EM 40, F1 50, cover-EM 60 on the same predictions. Poll: show two papers' numbers; "which is better?" (trick question). -->

---

## Open problems

1. Lifting the retrieval ceiling (train retrievers for agents)
2. Process rewards without gold evidence
3. Beyond short-answer QA
4. Latent vs. auditable
5. Memory across sessions
6. Multimodal *reading*
7. Defenses that don't break multi-hop reasoning
8. Cost as a first-class objective

---

## Three takeaways

1. **Retrieval decisions are becoming learned**: when (UR², QuCo-RAG), what (T²RAG, LatentRAG), how much (AutoSearch, HiPRAG)
2. **Retrieval quality is still the ceiling**: fix corpus, parsing and retriever first
3. **Trust and cost are first-class objectives**: FRANQ, InceptionRAG, SpecCache, AutoSearch

---

## Resources

- This repo: docs, paper notes, runnable code, reproduction guides
- KDD 2026 tutorial (Dong et al.): tutorial.lunadong.com
- Surveys: Gao 2024; RAG-Reasoning 2025; SoK Agentic RAG 2026; Multimodal RAG survey (ACL 2026)

<!-- Appendix slides to prepare: GRPO vs PPO; EM computation; GraphRAG indexing cost; latency breakdown; paper-status table. -->
