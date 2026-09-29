# Verification log

What was checked against primary sources, when, and what was corrected. **Last full pass: 29 September 2026.**

Method: each 2026 paper's ACL Anthology page and/or arXiv page was opened. For the eight deep-dives, plus SPARKLE, the full text (arXiv HTML or PDF) was read for method details and numbers. Code links were confirmed with `git ls-remote`.

## Corrections to earlier informal summaries

| Paper | Claim that circulated | Verified status |
|---|---|---|
| LatentRAG | "ACL 2026 paper" | **arXiv preprint only** (2605.06285, May 7, 2026), University of Amsterdam. About 90% lower latency across 7 benchmarks confirmed |
| UR² | — | **ACL 2026 main** (2026.acl-long.580). arXiv since August 2025 (2508.06165) |
| State-Aware RAG | "State-Aware RAG" as a title | The paper is titled **"Reasoning with Memory: Adaptive Information Management for Retrieval-Augmented Generation"**, **Findings ACL 2026** (2026.findings-acl.1834). +8.6% / +9.3% confirmed |
| QuCo-RAG | — | **Findings ACL 2026** (arXiv 2512.19134) |
| AutoSearch | — | **Findings ACL 2026** (2026.findings-acl.1399; arXiv 2604.17337) |
| T²RAG | — | **Findings ACL 2026** (2026.findings-acl.1310); arXiv August 2025 (2508.02435) |
| HiKEY | — | "Accepted to ACL 2026 Main" per the arXiv comment (2605.29606). +12.9% recall / +6.8% QA confirmed from the abstract and full text |
| HiGoE | "QA method" | **ACL 2026 main**. It targets long-context **summarization**, not QA |
| FRANQ | — | **Findings ACL 2026** (2026.findings-acl.338) |
| Chart-MRAG | "≈71% correctness, 81% coverage" vs repo "58.19% / 73.87%" | **ACL 2026 main.** The Anthology (camera-ready) abstract says **71.15% / 80.74%**; the CHARGE README's 58.19% / 73.87% appears to predate it. Quote the Anthology figures |
| SpecCache | — | **ACL 2026 main**. TTFT 2.17–3.95× and throughput 2.7–5.2× confirmed |
| SPARKLE | gains not checked | **ACL 2026 main** (2026.acl-long.1793). +9.17% in-domain / +2.85% out-of-domain average confirmed. Code: jyfang6/sparkle |
| QueryLink, EgoMemory | — | both **Findings ACL 2026** |
| Cross-modal conflict work | — | "When Image and Text Disagree" (CMC-Bench), single author, **MAGMaR 2026 workshop**. Treat as an early signal |
| RAG-on-a-Diet | — | **ACL 2026 main** (2026.acl-long.1562) |
| The Retrieval Bottleneck | read only from the abstract | **ACL 2026 main** (2026.acl-long.1478). Still abstract-level only; read the full paper before presenting its curves |
| "RAG 1.0 → 4.0" | presented as a taxonomy | **Not an established taxonomy.** Use modular / graph-enhanced / agentic (KDD 2026 tutorial, surveys), or label it as your own framing |

## Not verified or not found
- **ATIR:** no paper by that name found on the ACL Anthology or arXiv via search (September 2026). It is **excluded** from this repo until someone locates a primary source.
- **HiGoE metric values:** not quoted; the abstract gives no numbers.
- **SpecCache** full author list: the Anthology listing we saw was truncated.
- **Chart-MRAG** full author names: two appear in collapsed form in the Anthology metadata.

## Code availability (checked 29 September 2026)
Public: Search-R1, UR², AutoSearch, QuCo-RAG, T²RAG, HiGoE, QueryLink, SPARKLE, CHARGE (Chart-MRAG), and state-aware-rag (the repo exists; we did not check its contents).
Not found: LatentRAG, HiKEY, FRANQ (related toolkit: LM-Polygraph), SpecCache, RAG-on-a-Diet, The Retrieval Bottleneck, EgoMemory, CMC-Bench.

## Re-verification procedure
1. For each paper in [papers/README.md](../papers/README.md), open the Anthology or arXiv page. Check the venue, title and author list, and that every quoted number appears in the abstract or a named table.
2. Search arXiv and GitHub for newly released code.
3. Update the **Verified** row in the paper's note and the date at the top of this file.
