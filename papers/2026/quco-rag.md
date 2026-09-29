# QuCo-RAG: Quantifying Uncertainty from the Pre-training Corpus for Dynamic Retrieval-Augmented Generation

| | |
|---|---|
| **Authors** | Dehai Min, Kailin Zhang, Tongtong Wu, Lu Cheng |
| **Venue / status** | **Findings of ACL 2026** |
| **Links** | [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) · [code](https://github.com/ZhishanQ/QuCo-RAG) · [reproduction guide](../../experiments/quco-rag.md) · [toy triggers](../../code/ragkit/quco.py) |
| **Section** | 4, Learned retrieval policies (*when* to retrieve) |
| **Verified** | Venue from the repo; thresholds and numbers from arXiv HTML (September 2026) |

## TL;DR
To decide *when* to retrieve, stop asking the model how confident it is and **ask its training data** instead. QuCo-RAG retrieves when an entity is rare in the pre-training corpus, or when two entities the model just linked never co-occur there. On OLMo-2 it gains 5–12 EM points over dynamic-RAG baselines on multi-hop QA.

## 1. Problem and gap
Dynamic RAG methods (FLARE, DRAGIN, SeaKR, ETC) trigger retrieval from **model-internal signals** such as token probability, entropy or attention. But LLMs are poorly calibrated: they are often confidently wrong, which is exactly when retrieval is needed.

## 2. Key idea
Hallucinations are concentrated on **long-tail knowledge**, and the pre-training corpus tells you objectively what is long-tail. With [Infini-gram](https://infini-gram.readthedocs.io/), counting n-grams over OLMo-2's roughly 4-trillion-token corpus takes milliseconds.

## 3. Method
- **Stage 1, before generation.** Extract the entities in the question. If any has corpus frequency below τ_entity = 10³, retrieve with the original question. Results are stable for thresholds from 10³ to 10⁷.
- **Stage 2, during generation.** After each generated sentence, extract (head, relation, tail) triplets with a Qwen2.5-0.5B extractor fine-tuned on 40K GPT-4o-mini labels (89.9 F1). If head and tail never co-occur within a 1,000-token window (τ_cooc = 1), flag a likely hallucination: retrieve with "head ⊕ relation" and regenerate.
- **Retriever:** BM25 over a Wikipedia dump (about 21M passages), top-3.

## 4. Results (EM, 1,000 validation questions each)

| OLMo-2 | 2WikiMultihopQA | HotpotQA | Gain over best baseline |
|---|---|---|---|
| 7B | 32.7 | 35.3 | +7.4 / +5.6 |
| 13B | 41.7 | 35.0 | +12.0 / +5.3 |
| 32B | 46.8 | 41.6 | +9.4 / +10.8 |

- **Baselines:** no-RAG, single-round RAG, fixed-sentence RAG, FLARE, DRAGIN, ETC, SeaKR.
- **Efficiency:** 1.70 retrievals, 1.84 LLM calls and 87 extra tokens per question, the lowest among the dynamic methods compared.
- **Transfer:** the OLMo-2 corpus used as a *proxy* for Llama-3, Qwen2.5 and GPT-4.1/GPT-5-chat still gives up to +14 EM. The paper also validates on long-form and biomedical QA.

## 5. Limitations
- **(stated)** Lexical matching misses aliases ("NYC" vs "New York City"), which causes unnecessary retrievals.
- **(stated)** A static corpus cannot vouch for events after its snapshot.
- **(from the KDD 2026 tutorial's discussion)** The method needs access to, or a good proxy for, the pre-training corpus, and its value may shrink as corpora grow and fewer entities are "rare".
- **(ours)** Co-occurrence is necessary but not sufficient for truth: "Paris" and "Berlin" co-occur constantly, so a false claim linking two common entities passes Stage 2.

## 6. What changed vs. the previous approach
It is the first dynamic-RAG trigger grounded in **external, objective statistics** rather than the model's self-report, and it uses no training.

## 7. Discussion questions
1. How would QuCo-RAG behave on a closed model whose pre-training data differs a lot from OLMo-2's?
2. Could corpus statistics be a *reward signal* for RL search agents, for example a bonus for retrieving when an entity is rare?
