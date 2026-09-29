# 5. Latent retrieval: reasoning and searching without words

## 5.1 Why go latent?

Agentic RAG pays for its accuracy in latency. Measured in the LatentRAG paper:
- Search-R1 takes **16–22×** the inference time of naive RAG on multi-hop QA.
- About **90%** of that time is autoregressive decoding of *thoughts* and *sub-queries*, text the user never reads and the retriever immediately turns back into a vector.

So why decode it at all?

## 5.2 LatentRAG (arXiv, May 2026)

Deep-dive: [papers/2026/latentrag.md](../papers/2026/latentrag.md)

```
explicit:  hidden → "I need the director of Move (1970)" → tokenizer → retriever encoder → vector → search
latent:    hidden → [16 <query> token states, one forward pass] → projector → retriever encoder → vector → search
```

- 4 latent thought tokens and 16 latent query tokens per step, all computed in the **prefill** pass (parallel, not autoregressive).
- **Alignment loss:** the document distribution retrieved by the latent query should match the one retrieved by the *text* query it replaces (KL divergence, temperature 0.03).
- **Optional decoder** translates latents back to text for inspection. It is still 47–63% faster than the teachers even with decoding on.
- Trained by distillation from Search-R1 and AutoRefine trajectories (about 170K), LoRA on Qwen2.5-7B.
- **Result:** EM matches or slightly beats the teachers (43.46 vs 42.47 for Search-R1) at about 10% of the latency (593 ms vs 5,372 ms).

## 5.3 Related work

- **Latent reasoning** (Coconut, "chain of continuous thought", 2024) showed hidden states can carry reasoning steps. LatentRAG connects that to a *retriever*.
- **CLaRa** (Apple, [arXiv:2511.18659](https://arxiv.org/abs/2511.18659), 💻 [apple/ml-clara](https://github.com/apple/ml-clara)) unifies retrieval and generation in a shared continuous space using compressed document representations. It makes the *documents* latent, where LatentRAG makes the *queries and thoughts* latent.
- **REALM / RAG / Atlas** trained retrievers jointly with readers, but the interface stayed a text query.

## 5.4 Trade-offs to discuss

| | Explicit (Search-R1) | Latent (LatentRAG) |
|---|---|---|
| Latency | 16–22× naive RAG | about 2× naive RAG |
| Auditable queries | yes | only with the decoder |
| Swap the retriever | easy | needs re-alignment |
| Training | RL from outcome | SFT on teacher trajectories (bounded by the teacher) |
| Failure analysis | read the trace | probe vectors |

**Open question:** RL *in* latent space. The action is a continuous 16×d matrix. What is the policy distribution, and how do you explore?
