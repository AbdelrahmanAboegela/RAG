"""QuCo-RAG's two retrieval triggers on a toy 'pre-training corpus'.

    python code/examples/03_quco_trigger.py

To query OLMo-2's real pre-training corpus instead (network access needed):

    from ragkit.quco import InfiniGramStats
    stats = InfiniGramStats("v4_olmo-2-1124-13b-instruct_llama")
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import InMemoryCorpusStats, QuCoTrigger  # noqa: E402
from corpus import DOCS, QUESTION  # noqa: E402

# Pretend the model's pre-training corpus mentions Stuart Rosenberg often
# but Jean-Daniel Pollet only a couple of times.
PRETRAIN = DOCS[:2] * 50 + DOCS[2:4] * 2 + DOCS[6:]

if __name__ == "__main__":
    stats = InMemoryCorpusStats(PRETRAIN)
    trig = QuCoTrigger(stats, tau_entity=20)  # paper uses 10^3 on a 4T-token corpus

    d = trig.before_generation(QUESTION)
    print("Stage 1 (before generation):", d.retrieve, "-", d.reason)
    print("  entity frequencies:", d.evidence)

    # Suppose the model then generates two claims; the second is hallucinated.
    claims_ok = [("Stuart Rosenberg", "directed", "Move")]
    claims_bad = [("Jean-Daniel Pollet", "was born in", "Brazil")]
    for claims in (claims_ok, claims_bad):
        d = trig.during_generation(claims)
        print(f"Stage 2 on {claims}: retrieve={d.retrieve} ({d.reason}) query={d.query!r}")
