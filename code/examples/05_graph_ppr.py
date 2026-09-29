"""HippoRAG-style Personalized PageRank on the running example.

A *single* retrieval step reaches the nationality passages because PPR spreads
probability from the query entities (the two films) to their directors and on
to the directors' nationalities.

    python code/examples/05_graph_ppr.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import TripletGraph  # noqa: E402
from corpus import DOCS  # noqa: E402

# What an OpenIE pass (an LLM in HippoRAG) would extract, with the passage id.
TRIPLETS = [
    ("Move (1970)", "directed by", "Stuart Rosenberg", 0),
    ("Move (1970)", "starring", "Elliott Gould", 0),
    ("Stuart Rosenberg", "nationality", "American", 1),
    ("Stuart Rosenberg", "known for", "Cool Hand Luke", 1),
    ("Méditerranée (1963)", "directed by", "Jean-Daniel Pollet", 2),
    ("Jean-Daniel Pollet", "nationality", "French", 3),
    ("Jean-Daniel Pollet", "associated with", "French New Wave", 3),
    ("Move (2020 series)", "genre", "documentary", 4),
    ("Cool Hand Luke", "starring", "Paul Newman", 6),
    ("French New Wave", "emerged in", "France", 7),
    ("Elliott Gould", "nationality", "American", 8),
]

if __name__ == "__main__":
    g = TripletGraph(TRIPLETS)
    seeds = ["Move (1970)", "Méditerranée (1963)"]  # entities linked from the question
    print("Seeds:", seeds)
    for pid, score in g.rank_passages(seeds, k=5):
        print(f"  [{score:.3f}] {DOCS[pid][:90]}")
    print("\nBoth nationality passages (1 and 3) rank in the top 5 from one PPR call.")
