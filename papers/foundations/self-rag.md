# Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

| | |
|---|---|
| **Authors** | Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi |
| **Venue / status** | **ICLR 2024** (oral) |
| **Links** | [arXiv:2310.11511](https://arxiv.org/abs/2310.11511) · [code](https://github.com/AkariAsai/self-rag) |
| **Section** | 3, Classic toolkit ("the first learned retrieval policy") |

## TL;DR
Train one LM to emit **reflection tokens** that decide *whether* to retrieve and *judge* what it retrieved and what it wrote. At inference, those tokens gate retrieval and rank candidate outputs.

## 1. Problem
Standard RAG always retrieves a fixed k passages, even when retrieval is unnecessary or the passages are irrelevant, and it never checks whether its output is supported by them.

## 2. Key idea: four reflection tokens
| Token | Question it answers | Values |
|---|---|---|
| `[Retrieve]` | Should I retrieve now? | yes / no / continue |
| `[IsRel]` | Is this passage relevant? | relevant / irrelevant |
| `[IsSup]` | Is my segment supported by the passage? | fully / partially / no support |
| `[IsUse]` | Is the response useful overall? | 1–5 |

## 3. Method
1. **Critic:** GPT-4 labels a seed set with reflection tokens, and a critic model is distilled from those labels.
2. **Generator training:** the critic annotates a large instruction corpus offline, inserting reflection tokens and retrieved passages. The generator is trained with a standard next-token loss on this augmented corpus, so it learns to emit reflection tokens itself.
3. **Inference:**
   - When `[Retrieve]=yes`, retrieve k passages and generate a candidate segment per passage in parallel.
   - Score each candidate by a weighted sum of the reflection-token probabilities (IsRel, IsSup, IsUse).
   - Keep the best candidate (segment-level beam search). The weights are adjustable at test time, trading citation precision against fluency.

## 4. Results
It outperformed ChatGPT and retrieval-augmented Llama-2 on open-domain QA, reasoning, fact verification, and long-form generation with citations (ALCE), with large gains in citation precision.

## 5. Limitations
- The labels come from GPT-4 distillation, so the policy is bounded by the labeler.
- Retrieval decisions are made per segment, with no multi-hop planning.
- It is often weak as a reported baseline in 2025–26 papers (see SPARKLE's table), partly because of prompt and format mismatch.

## 6. What changed
It was the first model that **learned** when to retrieve and how to self-critique. Search-R1 later replaced *supervised reflection labels* with *outcome RL*.

## 7. Discussion
Self-RAG's `[IsSup]` token and FRANQ (2026) both judge support. What does FRANQ add that `[IsSup]` cannot express?
