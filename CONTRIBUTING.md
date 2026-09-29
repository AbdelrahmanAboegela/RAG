# Contributing

## Adding a paper
1. Copy [`papers/_TEMPLATE.md`](papers/_TEMPLATE.md) into `papers/<year>/<short-name>.md`.
2. Fill in every section. **Problem → key idea → method → results → limitations → what changed** is the core; keep the "what changed vs. the previous approach" answer to one sentence.
3. Fill in the **Verified** row honestly: say whether you read the abstract, the full text, or the code, and give the date.
4. Give the paper a **status label**: ACL/EMNLP/… main, Findings, workshop, or arXiv. Use the venue's own page, not a blog or aggregator.
5. Quote numbers only from the paper, and name the table or abstract they come from. If the paper and repo disagree, show both and prefer the camera-ready version.
6. Add a row to [`data/papers.csv`](data/papers.csv) and run `python tools/validate_papers.py`.
7. Add a row to [`papers/README.md`](papers/README.md) and to the relevant table in the top-level [`README.md`](README.md), and link the paper from the matching `docs/` chapter.

## Adding code
- `code/ragkit/` stays **standard-library only**, so anyone can run it. Heavy dependencies belong in `experiments/`.
- Each module's docstring must say which paper it illustrates and that it is **not** the official implementation.
- Add a test in `code/tests/` and run `python -m unittest discover -s code/tests`.

## Adding a reproduction guide
- Copy commands **verbatim from the official README** and note the date you copied them.
- Add paper-reported hyperparameters and expected numbers, with their source.

## Checks to run before a PR
```bash
python -m unittest discover -s code/tests
python tools/check_links.py              # offline: relative links and anchors
python tools/check_links.py --external   # network: GitHub repos + arXiv titles
python tools/validate_papers.py
python tools/run_notebook.py code/notebooks/ragkit_tour.ipynb
```
CI runs all of these except `--external` on every push.

## Style
- Plain, specific language. Don't use "revolutionary" or "state-of-the-art" without a number and a baseline.
- Link primary sources: ACL Anthology, arXiv, or the official GitHub repo.
