"""Tests for rerank, graph, rl, cache, raptor, router, evaluate, llm.

Run with:  python -m unittest discover -s code/tests   (from the repo root)
"""

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "examples"))

from ragkit import (  # noqa: E402
    AgenticRAG, GroundedAnswerCache, HashingEmbedder, HeuristicRouter, OpenAICompatibleLLM,
    ProximityReranker, RaptorTree, TripletGraph, cover_em, evaluate, group_relative_advantages,
    lost_in_the_middle_order, masked_policy_loss, mmr, retrieval_metrics, token_mask_from_steps,
)
from corpus import DOCS, QUESTION  # noqa: E402


class TestRerank(unittest.TestCase):
    def test_proximity_prefers_compact_match(self):
        r = ProximityReranker(window=4)
        near = "Pollet was a French filmmaker"
        far = "Pollet made films. " + "x " * 20 + "He was French."
        self.assertGreater(r.score("Pollet French", near), r.score("Pollet French", far))

    def test_mmr_avoids_duplicates(self):
        e = HashingEmbedder()
        docs = ["Pollet was French", "Pollet was French", "Rosenberg was American"]
        picked = mmr(e.embed("Pollet French Rosenberg American"), [e.embed(d) for d in docs], k=2, lam=0.5)
        self.assertEqual(len({docs[i] for i in picked}), 2)

    def test_lost_in_middle_order(self):
        self.assertEqual(lost_in_the_middle_order([1, 2, 3, 4, 5]), [1, 3, 5, 4, 2])
        self.assertEqual(lost_in_the_middle_order([]), [])


class TestGraph(unittest.TestCase):
    def test_ppr_reaches_two_hops(self):
        g = TripletGraph([("A", "r", "B", 0), ("B", "r", "C", 1), ("X", "r", "Y", 2)])
        ppr = g.personalized_pagerank(["A"])
        self.assertAlmostEqual(sum(ppr.values()), 1.0, places=6)
        self.assertGreater(ppr["c"], 0)
        self.assertEqual(ppr["x"], 0)
        self.assertEqual([p for p, _ in g.rank_passages(["A"], k=2)], [0, 1])

    def test_unknown_seed(self):
        self.assertEqual(TripletGraph([("A", "r", "B", 0)]).personalized_pagerank(["Z"]), {})


class TestRL(unittest.TestCase):
    def test_grpo_zero_mean(self):
        adv = group_relative_advantages([1, 0, 1, 0])
        self.assertAlmostEqual(sum(adv), 0.0, places=6)
        self.assertAlmostEqual(adv[0], 1.0, places=4)
        self.assertEqual(group_relative_advantages([1, 1, 1]), [0.0, 0.0, 0.0])

    def test_mask_excludes_retrieved_tokens(self):
        base = masked_policy_loss([-1.0, -1.0], [-1.0, -1.0], 1.0, [1, 1])
        self.assertAlmostEqual(base, -1.0)
        # changing a masked token's logprob must not change the loss
        self.assertAlmostEqual(masked_policy_loss([-1.0, -9.0], [-1.0, -1.0], 1.0, [1, 0]), base)

    def test_clipping(self):
        # ratio e^1 > 1.2 with positive advantage is clipped to 1.2
        self.assertAlmostEqual(masked_policy_loss([0.0], [-1.0], 1.0, [1]), -1.2)

    def test_mask_from_trajectory(self):
        turns = iter(["<search>q</search>", "<answer>a</answer>"])
        traj = AgenticRAG(lambda p: next(turns), lambda q, k: ["d"]).run("x")
        mask = token_mask_from_steps(traj.steps)
        self.assertIn(0, mask)
        self.assertEqual(mask[0], 1)


class TestCache(unittest.TestCase):
    def setUp(self):
        self.c = GroundedAnswerCache(sim_threshold=0.8)
        self.c.put("Who directed Move (1970)?", "Stuart Rosenberg", ["p0"], {"p0": 1})
        self.ev = {"p0": DOCS[0]}

    def test_hit(self):
        self.assertTrue(self.c.get("Who directed Move (1970)?", self.ev, {"p0": 1}).hit)

    def test_gates(self):
        self.assertEqual(self.c.get("Capital of France?", self.ev, {"p0": 1}).failed_gate, "similarity")
        self.assertEqual(self.c.get("Who directed Move (1970)?", {"p9": DOCS[1]}, {"p0": 1}).failed_gate,
                         "evidence_overlap")
        self.assertEqual(self.c.get("Who directed Move (1970)?", self.ev, {"p0": 2}).failed_gate,
                         "source_version")
        changed = {"p0": "Move is a 1970 film directed by someone else."}
        self.assertEqual(self.c.get("Who directed Move (1970)?", changed, {"p0": 1}).failed_gate,
                         "lexical_support")


class TestRaptor(unittest.TestCase):
    def test_tree_has_levels_and_search(self):
        t = RaptorTree(DOCS, branching=3)
        self.assertGreaterEqual(t.depth, 1)
        self.assertGreater(len(t.nodes), len(DOCS))
        self.assertEqual(len(t.search("French filmmaker", k=3)), 3)
        for n in t.nodes:
            if n.level > 0:
                self.assertTrue(n.children)


class TestRouter(unittest.TestCase):
    def test_routes(self):
        r = HeuristicRouter()
        self.assertEqual(r.route(QUESTION).strategy, "multi_step")
        self.assertEqual(r.route("Who directed Move (1970)?").strategy, "single_step")
        self.assertEqual(r.route("what is two plus two?").strategy, "no_retrieval")
        common = HeuristicRouter(freq=lambda e: 10 ** 6)
        self.assertEqual(common.route("Where is Paris?").strategy, "no_retrieval")


class TestEvaluate(unittest.TestCase):
    def test_metrics(self):
        self.assertEqual(cover_em("It was Stuart Rosenberg.", ["Stuart Rosenberg"]), 1.0)
        m = retrieval_metrics(["a", "b", "c"], ["b", "c"], ks=(1, 3))
        self.assertEqual((m["recall@1"], m["recall@3"], m["all@1"], m["all@3"], m["mrr"]), (0.0, 1.0, 0.0, 1.0, 0.5))

    def test_toy_run(self):
        with open(os.path.join(HERE, "..", "examples", "data", "toy_run.jsonl")) as f:
            rep = evaluate([json.loads(line) for line in f], ks=(1, 5))
        self.assertEqual(rep["n"], 5)
        self.assertEqual(rep["em"], 40.0)
        self.assertEqual(rep["cover_em"], 60.0)
        self.assertEqual(rep["avg_searches"], 2.0)


class _FakeChat(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        _FakeChat.last = body
        # Pretend the server stopped on "</search>" and stripped it.
        resp = {"choices": [{"message": {"content": "<think>x</think><search>Move 1970"},
                             "finish_reason": "stop"}]}
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


class TestLLMClient(unittest.TestCase):
    def test_openai_compatible_roundtrip(self):
        srv = HTTPServer(("127.0.0.1", 0), _FakeChat)
        th = threading.Thread(target=srv.serve_forever, daemon=True)
        th.start()
        try:
            llm = OpenAICompatibleLLM(f"http://127.0.0.1:{srv.server_port}/v1", "m",
                                      stop=["</search>", "</answer>"], append_stop=True, api_key="k")
            out = llm("hello")
            self.assertEqual(out, "<think>x</think><search>Move 1970</search>")
            self.assertEqual(_FakeChat.last["stop"], ["</search>", "</answer>"])
            self.assertEqual(_FakeChat.last["messages"][-1]["content"], "hello")
        finally:
            srv.shutdown()
            srv.server_close()


if __name__ == "__main__":
    unittest.main()
