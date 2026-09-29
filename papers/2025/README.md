# 2025: the RL-for-search turn

In January 2025, DeepSeek-R1 showed that outcome-reward RL elicits long reasoning. Within weeks, several groups applied the recipe to **reasoning + search**. This page catalogues the 2025 systems that the 2026 papers build on or compare against. The full note on the canonical one is [search-r1.md](search-r1.md).

| System | Month | Core idea | How it trains | Links |
|---|---|---|---|---|
| **Search-o1** | Jan 2025 | A large reasoning model (QwQ) issues searches mid-reasoning. A *Reason-in-Documents* module condenses results before they enter the chain. | Prompting only | [arXiv:2501.05366](https://arxiv.org/abs/2501.05366) · 💻 [sunnynexus/Search-o1](https://github.com/sunnynexus/Search-o1) |
| **R1-Searcher** | Mar 2025 | Two-stage outcome RL: first reward the *retrieval format*, then answer correctness. Generalises to online search. | RL (REINFORCE++ / GRPO) | [arXiv:2503.05592](https://arxiv.org/abs/2503.05592) · 💻 [RUCAIBox/R1-Searcher](https://github.com/RUCAIBox/R1-Searcher) |
| **Search-R1** | Mar 2025 | Interleaved `<search>` in reasoning; retrieved-token masking; EM reward. | PPO / GRPO (verl) | [note](search-r1.md) · 💻 [PeterGriffinJin/Search-R1](https://github.com/PeterGriffinJin/Search-R1) |
| **ReSearch** | Mar 2025 | Search operations are part of the reasoning chain; reflection and self-correction emerge without supervision. | GRPO | [arXiv:2503.19470](https://arxiv.org/abs/2503.19470) · 💻 [Agent-RL/ReSearch](https://github.com/Agent-RL/ReSearch) |
| **DeepResearcher** | Apr 2025 | End-to-end RL in the **real web** environment (not a local corpus), with multi-agent browsing. | GRPO | [arXiv:2504.03160](https://arxiv.org/abs/2504.03160) · 💻 [GAIR-NLP/DeepResearcher](https://github.com/GAIR-NLP/DeepResearcher) |
| **WebThinker** | Apr 2025 | A reasoning model that navigates the web and *drafts reports* while thinking; deep-research style. | RL-based training (iterative online DPO) | [arXiv:2504.21776](https://arxiv.org/abs/2504.21776) · 💻 [RUC-NLPIR/WebThinker](https://github.com/RUC-NLPIR/WebThinker) |
| **ZeroSearch** | May 2025 | Replace the real search engine with an **LLM that simulates search results** during RL, with a curriculum that degrades document quality. Removes API cost. | RL with a simulated environment | [arXiv:2505.04588](https://arxiv.org/abs/2505.04588) · 💻 [Alibaba-NLP/ZeroSearch](https://github.com/Alibaba-NLP/ZeroSearch) |
| **s3** | May 2025 | Train only a small **searcher**, with a frozen generator, rewarded by *Gain Beyond RAG*. Data-efficient (about 2.4K examples). State-Aware RAG's strongest RL baseline. | RL on the searcher only | [arXiv:2505.14146](https://arxiv.org/abs/2505.14146) · 💻 [pat-jj/s3](https://github.com/pat-jj/s3) |
| **Tongyi DeepResearch** and WebAgent family | 2025 | Open agentic deep-research models and data pipelines (WebWalker, WebDancer, WebSailor, …). | Agentic CPT + SFT + RL | 💻 [Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) · [Alibaba-NLP/WebAgent](https://github.com/Alibaba-NLP/WebAgent) |
| **CLaRa** (Apple) | Nov 2025 | Retrieval and generation unified in a **continuous latent space**, with compressed document representations trained jointly with the reader. The closest relative of LatentRAG. | Joint training | [arXiv:2511.18659](https://arxiv.org/abs/2511.18659) · 💻 [apple/ml-clara](https://github.com/apple/ml-clara) |

## Common recipe (and its common weaknesses)

**Recipe.** Qwen2.5-3B/7B · E5 over 2018 Wikipedia · train on NQ + HotpotQA · evaluate on NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue, Bamboogle · EM reward · PPO or GRPO · mask retrieved tokens.

**Weaknesses the 2026 papers attack.**
| Weakness | 2026 answer |
|---|---|
| Outcome-only reward gives no credit to good intermediate steps | AutoSearch (quality reward), State-Aware RAG (path reward) |
| Over-searching; no cost term | AutoSearch (depth), RAG-on-a-Diet (model size per hop) |
| Only works where retrieval always helps | UR² (difficulty-aware) |
| Must fine-tune the big LLM | SPARKLE, s3, State-Aware RAG (train a small proxy) |
| Text thoughts and queries are slow | LatentRAG (latent tokens) |
| Everyone tunes RL; nobody fixes retrieval | The Retrieval Bottleneck (retriever sets the ceiling) |
| The same 7 QA sets everywhere | still open; see [docs/12](../../docs/12-open-problems.md) |
