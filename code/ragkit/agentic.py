"""The Search-R1 interaction protocol, as a minimal loop.

Search-R1 (Jin et al., 2025) and most RL-trained search agents that followed
(R1-Searcher, ReSearch, ZeroSearch, AutoSearch, LatentRAG's teacher trajectories)
share one rollout format:

    <think> ... </think>
    <search> sub-query </search>
    <information> retrieved passages (inserted by the environment) </information>
    ... repeat ...
    <answer> final answer </answer>

The policy LLM generates until it closes a <search> or <answer> tag. The
environment runs the search and appends an <information> block. During RL, the
tokens inside <information> are *masked out of the loss*: the model is only
credited or blamed for tokens it produced. `Step.is_model_generated` records
exactly that split so you can see which spans would be trained on.

`llm` is any callable `prompt -> continuation`. Plug in vLLM, an API client, or
the scripted mock in examples/02_agentic_loop.py.
"""

import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional

_TAG = re.compile(r"<(search|answer)>(.*?)</\1>", re.S)

SYSTEM_PROMPT = (
    "Answer the given question. You must conduct reasoning inside <think> and </think> "
    "every time you get new information. If you lack knowledge, call a search engine with "
    "<search> query </search> and it will return results between <information> and "
    "</information>. You can search as many times as you want. When you have enough "
    "information, give the answer inside <answer> and </answer> without explanation.\n"
    "Question: {question}\n"
)


def parse_action(text: str):
    """Return ('search'|'answer', payload) for the first closed action tag, else (None, None)."""
    m = _TAG.search(text)
    if not m:
        return None, None
    return m.group(1), m.group(2).strip()


@dataclass
class Step:
    text: str
    is_model_generated: bool  # False for <information> blocks -> masked from the RL loss
    action: Optional[str] = None
    payload: Optional[str] = None


@dataclass
class Trajectory:
    question: str
    steps: List[Step] = field(default_factory=list)
    answer: Optional[str] = None

    @property
    def num_searches(self) -> int:
        return sum(1 for s in self.steps if s.action == "search")

    @property
    def search_queries(self):
        return [s.payload for s in self.steps if s.action == "search"]

    def transcript(self) -> str:
        return "".join(s.text for s in self.steps)


class AgenticRAG:
    def __init__(self, llm: Callable[[str], str], retrieve: Callable[[str, int], List[str]],
                 max_turns: int = 4, top_k: int = 3, prompt_template: str = SYSTEM_PROMPT):
        self.llm = llm
        self.retrieve = retrieve
        self.max_turns = max_turns
        self.top_k = top_k
        self.prompt_template = prompt_template

    @staticmethod
    def format_information(docs: List[str]) -> str:
        body = "\n".join(f"Doc {i + 1}: {d}" for i, d in enumerate(docs))
        return f"\n<information>{body}</information>\n"

    def run(self, question: str) -> Trajectory:
        traj = Trajectory(question)
        prompt = self.prompt_template.format(question=question)
        for _ in range(self.max_turns + 1):
            out = self.llm(prompt + traj.transcript())
            action, payload = parse_action(out)
            if action is None:
                traj.steps.append(Step(out, True))
                break
            # Truncate the model output right after the first closed action tag,
            # exactly as Search-R1 uses stop sequences on </search> and </answer>.
            end = out.find(f"</{action}>") + len(action) + 3
            traj.steps.append(Step(out[:end], True, action, payload))
            if action == "answer":
                traj.answer = payload
                break
            docs = self.retrieve(payload, self.top_k)
            traj.steps.append(Step(self.format_information(docs), False))
        return traj
