# Chart-MRAG: Benchmarking Multimodal Retrieval Augmented Generation on Chart-based Documents

| | |
|---|---|
| **Authors** | As listed on the ACL Anthology: "Ymyang", Jiang Zhong, Li Jin, Xiao Sun, Jingwang Huang, "Gaojinpeng", Qing Liu, Yang Bai, Jingyuan Zhang, Rui Jiang, Qin Lei, Kaiwen Wei |
| **Venue / status** | **ACL 2026 main** (Long) |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.acl-long.1164/) · [CHARGE repo](https://github.com/Nomothings/CHARGE) · dataset on HF: `ymyang/chart-mrag` · [usage notes](../../experiments/chart-mrag.md) |
| **Section** | 9, Multimodal |
| **Verified** | Anthology abstract and repo README (September 2026) |

> Two author names appear in collapsed form in the Anthology metadata ("Ymyang", "Gaojinpeng"). Take full names from the PDF before putting them on a slide.

**Contribution.**
- **CHARGE**, a semi-automatic pipeline for generating chart-grounded QA (keypoint extraction, cross-modal verification, keypoint-based generation).
- **Chart-MRAG Bench**, with 4,738 QA pairs across 8 domains (3,026 with charts).

**Findings.**
1. Unified multimodal embedding retrievers struggle when the evidence is in charts.
2. Even **with ground-truth retrieval**, state-of-the-art MLLMs reach only **71.15% Correctness and 80.74% Coverage** (camera-ready abstract).
3. MLLMs show **text-over-visual bias**: when text and chart are both present, they lean on the text.

**Numbers caveat.** The CHARGE README reports **58.19% / 73.87%** (apparently from an earlier version). Quote the Anthology figures.
