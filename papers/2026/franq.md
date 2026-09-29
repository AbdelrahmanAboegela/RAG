# FRANQ: Faithfulness-Aware Uncertainty Quantification for Fact-Checking the Output of Retrieval-Augmented Generation

| | |
|---|---|
| **Authors** | Ekaterina Fadeeva, Aleksandr Rubashevskii, Dzianis Piatrashyn, Roman Vashurin, Shehzaad Dhuliawala, Artem Shelmanov, Timothy Baldwin, Preslav Nakov, Mrinmaya Sachan, Maxim Panov |
| **Venue / status** | **Findings of ACL 2026**, pp. 6814–6836 |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.338/) · [arXiv:2505.21072](https://arxiv.org/abs/2505.21072) · related toolkit: [LM-Polygraph](https://github.com/IINemo/lm-polygraph) |
| **Section** | 8, Evidence and trust |
| **Verified** | Abstract on the ACL Anthology (September 2026) |

**Problem.** Hallucination detectors for RAG usually equate "unsupported by the retrieved context" with "wrong". But a statement can be **factually correct yet unfaithful** (the model knew it from pre-training), or **faithful yet false** (the retrieved document was wrong).

**Method.** FRANQ estimates the probability that a claim is *factual* by decomposing it:

P(true) = P(faithful) · P(true | faithful) + (1 − P(faithful)) · P(true | unfaithful)

A different uncertainty-quantification technique is used for each branch. For faithful claims, trust grounding in the context; for unfaithful ones, fall back on the model's parametric uncertainty.

**Data.** A new long-form QA dataset annotated separately for **factuality** and **faithfulness**.

**Result.** More accurate detection of factual errors than existing UQ and hallucination detectors, across datasets, tasks and LLMs.

**What changed.** It separates two properties that most RAG evaluation conflates. This matters for the knowledge-conflict and poisoning discussion in [docs/08](../../docs/08-evidence-and-trust.md).
