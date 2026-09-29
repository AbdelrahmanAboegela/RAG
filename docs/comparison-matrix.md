# Method comparison matrix

A side-by-side view of **what each method changes** and **what it costs**. It does *not* compare accuracy numbers across papers, because those are not comparable ([11](11-evaluation.md#112-why-you-cant-compare-numbers-across-papers)).

Legend: ✅ core contribution · ◐ partial / secondary · — not addressed. Training: **none** (prompting / training-free), **SFT**, **RL**, **SFT→RL**.

## Retrieval policy methods

| Method | Year / venue | When | What (query) | How much | How to use | Cost | What is trained | Training | Needs gold evidence? | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| FLARE | 2023 EMNLP | ✅ | ◐ | — | — | — | nothing | none | no | ✅ |
| Self-RAG | 2024 ICLR | ✅ | — | — | ✅ critique | — | generator | SFT (GPT-4 labels) | no | ✅ |
| IRCoT | 2023 ACL | ◐ every step | ✅ CoT as query | — | — | — | nothing | none | no | ✅ |
| Adaptive-RAG | 2024 NAACL | ✅ per query | — | ◐ | — | ◐ | classifier | SFT | no | ✅ |
| DRAGIN | 2024 ACL | ✅ | ✅ | — | — | — | nothing | none | no | ✅ |
| Search-R1 | 2025 | ✅ | ✅ | ◐ | — | — | policy LLM | RL | no | ✅ |
| s3 | 2025 | ✅ | ✅ | — | — | — | small searcher | RL | no | ✅ |
| StepSearch | 2025 | ✅ | ✅ | ◐ | — | ◐ | policy LLM | step-wise PPO | yes (sub-question trajectories) | ✅ |
| **UR²** | 2026 ACL | ✅ whether | ✅ | — | ✅ summaries | — | policy LLM | RL (2-stage) | no | ✅ |
| **AutoSearch** | 2026 Findings | ✅ | ✅ | ✅ depth | — | ✅ | policy LLM | RL | no (needs gold *answer*) | ✅ |
| **HiPRAG** | 2026 ICLR | ✅ per step | ✅ | ✅ | — | ✅ | policy LLM | RL + process reward | no | — |
| **QuCo-RAG** | 2026 Findings | ✅ corpus stats | ◐ | — | — | ✅ | tiny entity extractor | SFT (extractor only) | no | ✅ |
| **SPARKLE** | 2026 ACL | ✅ | ✅ | — | ✅ triplet selection | — | 3B proxy | RL (PPO) | no | ✅ |
| **RAG-on-a-Diet** | 2026 ACL | ◐ termination | — | ✅ | — | ✅ money | router agent | RL | no | — |
| **CIPO** | 2026 arXiv | — | — | — | ✅ evidence use | — | policy LLM | RL | no | — |

## Representation, memory and efficiency methods

| Method | Year / venue | Unit / structure | Index cost | Query-time mechanism | Trained? | Code |
|---|---|---|---|---|---|---|
| GraphRAG | 2024 | entity graph + community reports | very high | map-reduce over reports | no | ✅ |
| HippoRAG 2 | 2025 ICML | OpenIE KG + passage nodes | high | PPR | no | ✅ |
| RAPTOR | 2024 ICLR | cluster-summary tree | high | collapsed-tree search | no | ✅ |
| **T²RAG** | 2026 Findings | flat triplet index | medium | placeholder-triplet resolution loop | no | ✅ |
| **TH-RAG** | 2026 ACL | topic hierarchy over triplets | see paper | topic-hierarchical retrieval | see paper | — |
| **HiKEY** | 2026 ACL | parsed document tree, multimodal units | high (LVLM parsing) | doc → section → unit routing | no | — |
| **HiGoE** | 2026 ACL | proposition–evidence graph | high | PPR + GAT selection | GAT | ✅ |
| **State-Aware RAG** | 2026 Findings | working memory | none | extractor curates memory each hop | 4B extractor (SFT→GRPO) | repo |
| **QueryLink** | 2026 Findings | aligned query/memory views | medium | alignment + coherent chunks | — | ✅ |
| **LatentRAG** | 2026 arXiv | latent queries/thoughts | none | one forward pass per step | LoRA + retriever (SFT) | — |
| **SpecCache** | 2026 ACL | precomputed KV | medium | small model picks tokens to recompute | no | — |

## Which method for which problem?

| Your problem | Start with | Then consider |
|---|---|---|
| Single-hop factual QA | hybrid retrieval + reranker | QuCo-style trigger to skip retrieval |
| Multi-hop factual QA | IRCoT or a prompted search agent | T²RAG; RL agent (Search-R1 → AutoSearch/HiPRAG) |
| Mixed tasks (math, medical, QA) | router | UR² |
| Big frozen LLM, can't fine-tune | prompted agent | SPARKLE / s3 / State-Aware RAG (train a small controller) |
| Latency-critical agentic RAG | cap search depth | AutoSearch; LatentRAG |
| Global questions over a corpus | GraphRAG / LightRAG | RAPTOR, TH-RAG |
| Structured PDFs, tables, figures | structure-aware parsing | HiKEY; ColPali |
| Long conversations / agent memory | Mem0 / A-MEM | QueryLink, Memory-R1 |
| High-stakes answers | citations + abstention | FRANQ-style verification |
