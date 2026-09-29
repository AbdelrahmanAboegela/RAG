"""Validate data/papers.csv against the repo.

Checks: required columns, allowed status values, unique keys, arXiv/Anthology ID
formats, that each note file exists, and that each note's **Venue / status** row
agrees with the CSV status. Standard library only.

    python tools/validate_papers.py
"""

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUSES = {"acl-main": "ACL 2026 main", "acl-findings": "Findings of ACL 2026",
            "workshop": "Workshop", "arxiv": "arXiv", "other": None}
ARXIV = re.compile(r"^\d{4}\.\d{4,5}$")
ANTH = re.compile(r"^\d{4}\.[a-z-]+\.\d+$")


def main() -> int:
    errors = []
    with open(os.path.join(ROOT, "data", "papers.csv"), newline="") as f:
        rows = list(csv.DictReader(f))
    keys = set()
    for i, r in enumerate(rows, start=2):
        where = f"papers.csv:{i} ({r.get('key')})"
        if r["key"] in keys:
            errors.append(f"{where}: duplicate key")
        keys.add(r["key"])
        if r["status"] not in STATUSES:
            errors.append(f"{where}: unknown status {r['status']!r}")
        if r["status"] == "other" and not r["venue_detail"]:
            errors.append(f"{where}: status 'other' needs venue_detail")
        if r["arxiv"] and not ARXIV.match(r["arxiv"]):
            errors.append(f"{where}: bad arXiv id {r['arxiv']!r}")
        if r["anthology"] and not ANTH.match(r["anthology"]):
            errors.append(f"{where}: bad Anthology id {r['anthology']!r}")
        if not (r["arxiv"] or r["anthology"]):
            errors.append(f"{where}: needs an arXiv or Anthology id")
        note = os.path.join(ROOT, r["note"])
        if not os.path.exists(note):
            errors.append(f"{where}: missing note {r['note']}")
            continue
        text = open(note).read()
        venue_row = next((line for line in text.splitlines() if line.startswith("| **Venue")), "")
        label = STATUSES[r["status"]]
        if label and label.split()[0] not in venue_row:
            errors.append(f"{where}: note venue row {venue_row!r} does not mention {label!r}")
        if r["anthology"] and r["anthology"] not in text:
            errors.append(f"{where}: note does not link Anthology id {r['anthology']}")
        if r["arxiv"] and r["arxiv"] not in text:
            errors.append(f"{where}: note does not link arXiv id {r['arxiv']}")
    for e in errors:
        print("ERROR", e)
    print(f"{len(rows)} papers checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
