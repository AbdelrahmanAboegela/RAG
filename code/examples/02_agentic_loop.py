"""The Search-R1 rollout protocol with a scripted policy, plus an AutoSearch reward.

A real run replaces `ScriptedPolicy` with an RL-trained LLM (see
experiments/search-r1.md). The script is deliberately suboptimal: it performs
one redundant search at the end, so the AutoSearch reward flags over-searching.

    python code/examples/02_agentic_loop.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from ragkit import AgenticRAG, HybridRetriever, autosearch_reward, exact_match  # noqa: E402
from corpus import DOCS, GOLD, QUESTION  # noqa: E402


class ScriptedPolicy:
    """Emits one pre-written turn per call, like a policy that always takes the same actions."""

    TURNS = [
        "<think>I need the director of Move (1970).</think><search>Move 1970 film director</search>",
        "<think>Stuart Rosenberg. Now Méditerranée.</think><search>Méditerranée 1963 film director</search>",
        "<think>Jean-Daniel Pollet. Nationalities?</think><search>Stuart Rosenberg nationality</search>",
        "<think>Rosenberg is American.</think><search>Jean-Daniel Pollet nationality</search>",
        "<think>Pollet is French. Let me double-check Rosenberg.</think><search>Stuart Rosenberg born</search>",
        "<think>American vs French.</think><answer>no</answer>",
    ]

    def __init__(self):
        self.i = 0

    def __call__(self, prompt: str) -> str:
        out = self.TURNS[min(self.i, len(self.TURNS) - 1)]
        self.i += 1
        return out


if __name__ == "__main__":
    retriever = HybridRetriever(DOCS)
    agent = AgenticRAG(ScriptedPolicy(), retriever.retrieve_text, max_turns=6, top_k=2)
    traj = agent.run(QUESTION)

    for s in traj.steps:
        tag = "MODEL " if s.is_model_generated else "ENV   "
        print(f"{tag}| {s.text.strip()[:110]}")
    print(f"\nAnswer: {traj.answer}  EM={exact_match(traj.answer, GOLD)}  searches={traj.num_searches}")
    print("ENV rows are <information> blocks: masked out of the policy-gradient loss in Search-R1.")

    # AutoSearch needs an intermediate answer after each search. For a comparison
    # question the answer only becomes derivable after hop 4.
    intermediate = ["unknown", "unknown", "unknown", "no", "no"]
    r = autosearch_reward(intermediate, traj.answer, GOLD)
    print(f"\nAutoSearch reward: {r}")
    print("t_c=4 but the agent searched 5 times -> 'over-search' regime, efficiency < 0.")
