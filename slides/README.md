# Slides

[`advanced-rag.md`](advanced-rag.md) is a 47-slide lecture deck in [Marp](https://marp.app/) Markdown. It follows [docs/lecture-outline.md](../docs/lecture-outline.md), uses the running example throughout, and has **speaker notes, polls and live-demo cues** in HTML comments.

## Render
```bash
# VS Code: install the "Marp for VS Code" extension and open the file, or:
npx @marp-team/marp-cli slides/advanced-rag.md -o advanced-rag.html
npx @marp-team/marp-cli slides/advanced-rag.md --pptx -o advanced-rag.pptx   # PowerPoint (slides are images; add --pptx-editable for experimental editable output)
npx @marp-team/marp-cli slides/advanced-rag.md --pdf  -o advanced-rag.pdf
```

## Live demos referenced in the notes
| Slide | Command |
|---|---|
| Failure modes | `python code/examples/01_hybrid_retrieval.py` |
| Graphs | `python code/examples/05_graph_ppr.py` |
| Search-R1 | `python code/examples/02_agentic_loop.py`, `python code/examples/06_grpo.py` |
| QuCo-RAG | `python code/examples/03_quco_trigger.py` |
| T²RAG | `python code/examples/04_t2rag.py` |
| Evaluation | `python code/examples/08_evaluate.py` |

## Before presenting
- Every number on the slides comes from the paper notes in [`papers/`](../papers/). Re-check the [verification log](../docs/verification-log.md) the week before.
- For a 90-minute slot, drop the long-term memory, graph-RAG-2026, multimodal and deep-research slides, and fold "don't compare numbers" into Section 4.
