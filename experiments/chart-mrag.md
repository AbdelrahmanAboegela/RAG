# Using Chart-MRAG Bench

**Repo:** [Nomothings/CHARGE](https://github.com/Nomothings/CHARGE) · **Data:** Hugging Face `ymyang/chart-mrag` · **Paper:** [ACL 2026 main](https://aclanthology.org/2026.acl-long.1164/) · **Notes:** [papers/2026/chart-mrag.md](../papers/2026/chart-mrag.md)

```python
from datasets import load_dataset
dataset = load_dataset("ymyang/chart-mrag")
sample = dataset[0]   # query, ground-truth answer, chart image, relevant text, extracted keypoints
```

Size: 4,738 QA pairs across 8 domains (3,026 with charts, 1,712 without).

## Which number to quote

The **ACL Anthology abstract** (camera-ready) reports that state-of-the-art MLLMs reach **71.15% Correctness and 80.74% Coverage** with ground-truth retrieval. The **CHARGE repo README** still reports **58.19% and 73.87%**, which appear to come from an earlier version of the paper. Quote the camera-ready figures, and cite the Anthology page.

Metrics are keypoint-based: *Correctness* checks whether the stated keypoints are right, and *Coverage* checks how many gold keypoints the answer includes.
