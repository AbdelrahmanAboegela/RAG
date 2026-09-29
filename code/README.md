# `code/`: reference implementations

Small, dependency-free Python (3.8+, standard library only) that shows **the mechanism** of the key ideas in this repo. Each module is a few dozen lines so you can read it in one sitting, step through it in a debugger, and change it.

> These are teaching implementations. They are **not** the authors' code and do **not** reproduce paper numbers. To reproduce results, use the official repositories; [`../experiments/`](../experiments/) has setup guides for them.

## Quick start

```bash
# from the repo root
python -m unittest discover -s code/tests      # 33 tests, runs in <1 s
python code/examples/01_hybrid_retrieval.py    # naive RAG: BM25 vs dense vs RRF
python code/examples/02_agentic_loop.py        # Search-R1 protocol + AutoSearch reward
python code/examples/03_quco_trigger.py        # QuCo-RAG's corpus-statistics triggers
python code/examples/04_t2rag.py               # T²RAG's placeholder-triplet loop
python code/examples/05_graph_ppr.py           # HippoRAG-style Personalized PageRank
python code/examples/06_grpo.py                # GRPO advantages + masked PPO loss
python code/examples/07_rerank_and_order.py    # rerank, MMR, lost-in-the-middle ordering
python code/examples/08_evaluate.py            # EM vs F1 vs cover-EM vs retrieval metrics
cd code && python -m ragkit examples/data/toy_run.jsonl   # evaluate any JSONL run
```

All examples share one **running example** ([`examples/corpus.py`](examples/corpus.py)):

> *Are the directors of Move (1970) and Méditerranée (1963) from the same country?*

It is a four-hop comparison question in the style of 2WikiMultihopQA, and it is the example in Figure 1 of the State-Aware RAG paper. The toy corpus contains distractors: a different show called *Move*, a page about the Rosenberg surname, and an unrelated 1963 page.

## Modules

| Module | Idea | Paper(s) | Docs |
|---|---|---|---|
| [`metrics.py`](ragkit/metrics.py) | SQuAD-style normalisation, EM, token F1 | used by almost all QA papers | [11-evaluation](../docs/11-evaluation.md) |
| [`text.py`](ragkit/text.py) | tokenisation, fixed-window and sentence chunking | DPR-style 100-word passages | [01-foundations](../docs/01-foundations.md) |
| [`bm25.py`](ragkit/bm25.py) | Okapi BM25 | Robertson & Zaragoza 2009 | [01-foundations](../docs/01-foundations.md) |
| [`dense.py`](ragkit/dense.py) | toy bi-encoder (feature hashing), cosine search; plug in a real embedder | DPR, E5, BGE | [01-foundations](../docs/01-foundations.md) |
| [`fusion.py`](ragkit/fusion.py), [`rrf_hybrid.py`](ragkit/rrf_hybrid.py) | Reciprocal Rank Fusion, hybrid retriever | Cormack et al. 2009 | [01-foundations](../docs/01-foundations.md) |
| [`agentic.py`](ragkit/agentic.py) | `<think>/<search>/<information>/<answer>` rollout loop, marking which spans are masked from the RL loss | Search-R1 and successors | [04-learned-retrieval-policies](../docs/04-learned-retrieval-policies.md) |
| [`autosearch_reward.py`](ragkit/autosearch_reward.py) | minimal sufficient search depth; base, efficiency and quality rewards | AutoSearch (Findings ACL 2026) | [papers/2026/autosearch.md](../papers/2026/autosearch.md) |
| [`quco.py`](ragkit/quco.py) | entity-frequency and co-occurrence retrieval triggers; optional Infini-gram client | QuCo-RAG (Findings ACL 2026) | [papers/2026/quco-rag.md](../papers/2026/quco-rag.md) |
| [`t2rag.py`](ragkit/t2rag.py) | resolved / searchable / fuzzy triplets, iterative binding | T²RAG (Findings ACL 2026) | [papers/2026/t2rag.md](../papers/2026/t2rag.md) |
| [`rerank.py`](ragkit/rerank.py) | joint query–doc reranker (toy cross-encoder), MMR, lost-in-the-middle ordering | Carbonell & Goldstein 1998; Liu et al. 2024 | [01-foundations](../docs/01-foundations.md) |
| [`graph.py`](ragkit/graph.py) | triplet graph + Personalized PageRank passage ranking | HippoRAG | [papers/foundations/hipporag.md](../papers/foundations/hipporag.md) |
| [`raptor.py`](ragkit/raptor.py) | recursive k-means + summary tree, collapsed-tree search | RAPTOR | [papers/foundations/raptor.md](../papers/foundations/raptor.md) |
| [`rl.py`](ragkit/rl.py) | GRPO group-relative advantages, PPO-clip loss with retrieved-token mask | Search-R1, DeepSeekMath | [04-learned-retrieval-policies](../docs/04-learned-retrieval-policies.md) |
| [`router.py`](ragkit/router.py) | no / single / multi-step retrieval routing | Adaptive-RAG, UR², Self-Route | [14-long-context-vs-rag](../docs/14-long-context-vs-rag.md) |
| [`cache.py`](ragkit/cache.py) | answer cache with similarity, evidence-overlap, version and support gates | GroundedCache, FinCacheServe (2026) | [10-efficiency](../docs/10-efficiency.md) |
| [`evaluate.py`](ragkit/evaluate.py) | EM, F1, cover-EM, Recall@k, All@k, MRR, avg searches from JSONL | — | [11-evaluation](../docs/11-evaluation.md) |
| [`llm.py`](ragkit/llm.py) | stdlib client for any OpenAI-compatible endpoint (vLLM, SGLang, …) with stop-tag restoration | — | below |

## Plugging in real models

The quickest path is a local vLLM server plus `ragkit.llm.OpenAICompatibleLLM`:

```bash
vllm serve Qwen/Qwen2.5-7B-Instruct --port 8000
```
```python
from ragkit import AgenticRAG, HybridRetriever, OpenAICompatibleLLM
llm = OpenAICompatibleLLM("http://localhost:8000/v1", "Qwen/Qwen2.5-7B-Instruct",
                          stop=["</search>", "</answer>"], append_stop=True)
agent = AgenticRAG(llm, HybridRetriever(my_docs).retrieve_text)
```

To use a trained Search-R1 checkpoint, serve it the same way; the tag protocol in `agentic.py` matches Search-R1's.


Every component that would call an LLM or an embedding model takes a plain function, so you can swap in a real one:

```python
from ragkit import AgenticRAG, HybridRetriever

class ST:  # any object with .embed(text) -> list[float]
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.m = SentenceTransformer("intfloat/e5-base-v2")
    def embed(self, text):
        return self.m.encode("query: " + text).tolist()

retriever = HybridRetriever(my_docs, embedder=ST())

def llm(prompt: str) -> str:          # vLLM / OpenAI / Anthropic / HF generate
    return client.generate(prompt, stop=["</search>", "</answer>"]) + "</search>"  # re-append the stop tag

agent = AgenticRAG(llm, retriever.retrieve_text, max_turns=4, top_k=3)
print(agent.run("Who directed Move (1970)?").answer)
```

`ragkit.quco.InfiniGramStats("v4_olmo-2-1124-13b-instruct_llama")` queries OLMo-2's pre-training corpus through the public [Infini-gram API](https://infini-gram.readthedocs.io/en/latest/api.html). This needs network access; the tests use `InMemoryCorpusStats`.

## Exercises

1. **Chunking.** Re-chunk `DOCS` with `chunk_words(size=8, overlap=2)` and re-run example 01. Which facts get split across chunks?
2. **RRF `k`.** Set `k=1` in `reciprocal_rank_fusion`. What happens to documents that only one retriever ranks highly?
3. **Over-searching.** In example 02, delete the redundant fifth search. How do the `efficiency` and `total` rewards change? Then make the agent answer after hop 3 with the wrong answer and compare.
4. **QuCo thresholds.** Vary `tau_entity` in example 03 between 1 and 200. Where does Stage 1 stop firing? Why is the paper's threshold (10³) stable across 10³–10⁷ on a 4T-token corpus but would be meaningless here?
5. **T²RAG failure.** Make `resolve` return `None` for the Pollet nationality. What does the loop do, and what would the paper's fallback to source chunks buy you?
