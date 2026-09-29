"""Run with:  python -m unittest discover -s code/tests   (from the repo root)"""

import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "examples"))

from ragkit import (  # noqa: E402
    AgenticRAG, BM25, HybridRetriever, InMemoryCorpusStats, QuCoTrigger, T2RAG, Triplet,
    autosearch_reward, chunk_sentences, chunk_words, classify, exact_match, f1_score,
    minimal_sufficient_depth, parse_action, reciprocal_rank_fusion,
)
from corpus import DOCS, GOLD, QUESTION  # noqa: E402


class TestMetrics(unittest.TestCase):
    def test_em_normalises(self):
        self.assertEqual(exact_match("The  Eiffel Tower!", "eiffel tower"), 1.0)
        self.assertEqual(exact_match("Paris", ["London", "paris"]), 1.0)
        self.assertEqual(exact_match("Paris, France", "Paris"), 0.0)

    def test_f1(self):
        self.assertAlmostEqual(f1_score("Paris France", "Paris"), 2 / 3)
        self.assertEqual(f1_score("", ""), 1.0)
        self.assertEqual(f1_score("x", "y"), 0.0)


class TestChunking(unittest.TestCase):
    def test_word_chunks_overlap(self):
        chunks = chunk_words(" ".join(str(i) for i in range(10)), size=4, overlap=2)
        self.assertEqual(chunks[0], "0 1 2 3")
        self.assertEqual(chunks[1], "2 3 4 5")
        self.assertTrue(chunks[-1].endswith("9"))

    def test_sentence_chunks_do_not_split(self):
        chunks = chunk_sentences("A b c. D e f. G h i.", max_words=6)
        self.assertEqual(chunks, ["A b c. D e f.", "G h i."])


class TestRetrieval(unittest.TestCase):
    def test_bm25_finds_relevant(self):
        top = BM25(DOCS).search("Jean-Daniel Pollet nationality filmmaker", 1)[0][0]
        self.assertIn("Jean-Daniel Pollet was a French", DOCS[top])

    def test_rrf(self):
        fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "a", "d"]], k=60)
        self.assertEqual({fused[0][0], fused[1][0]}, {"a", "b"})
        self.assertEqual(fused[-1][0], "d")

    def test_hybrid_returns_k(self):
        self.assertEqual(len(HybridRetriever(DOCS).search("Stuart Rosenberg", 3)), 3)


class TestAgentic(unittest.TestCase):
    def test_parse_action(self):
        self.assertEqual(parse_action("<think>x</think><search> q </search>"), ("search", "q"))
        self.assertEqual(parse_action("<answer>no</answer>"), ("answer", "no"))
        self.assertEqual(parse_action("no tags"), (None, None))

    def test_loop_masks_information(self):
        turns = iter(["<search>Move 1970 director</search>", "<answer>no</answer>"])
        agent = AgenticRAG(lambda p: next(turns), HybridRetriever(DOCS).retrieve_text, top_k=1)
        traj = agent.run(QUESTION)
        self.assertEqual(traj.answer, "no")
        self.assertEqual(traj.num_searches, 1)
        self.assertEqual([s.is_model_generated for s in traj.steps], [True, False, True])
        self.assertIn("<information>", traj.steps[1].text)

    def test_loop_stops_at_max_turns(self):
        agent = AgenticRAG(lambda p: "<search>x</search>", lambda q, k: ["d"], max_turns=2)
        self.assertIsNone(agent.run("q").answer)


class TestAutoSearch(unittest.TestCase):
    def test_depth(self):
        self.assertEqual(minimal_sufficient_depth(["a", "no", "no"], "no"), 2)
        self.assertIsNone(minimal_sufficient_depth(["a", "b"], "no"))

    def test_regimes_ordered(self):
        eff = autosearch_reward(["x", "no"], "no", GOLD)
        over = autosearch_reward(["x", "no", "no", "no"], "no", GOLD)
        under = autosearch_reward(["x", "y"], "y", GOLD)
        self.assertEqual((eff["regime"], over["regime"], under["regime"]),
                         ("effective", "over-search", "under-search"))
        self.assertGreater(eff["total"], over["total"])
        self.assertGreater(over["total"], under["total"])


class TestQuCo(unittest.TestCase):
    def setUp(self):
        self.stats = InMemoryCorpusStats(DOCS[:2] * 50 + DOCS[2:4])
        self.trig = QuCoTrigger(self.stats, tau_entity=20)

    def test_counts(self):
        self.assertEqual(self.stats.count("Stuart Rosenberg"), 100)
        self.assertEqual(self.stats.count("Jean-Daniel Pollet"), 2)
        self.assertGreater(self.stats.cooccur("Pollet", "French"), 0)
        self.assertEqual(self.stats.cooccur("Pollet", "Brazil"), 0)

    def test_stage1_flags_rare_entity(self):
        d = self.trig.before_generation(QUESTION)
        self.assertTrue(d.retrieve)
        self.assertIn("Méditerranée", d.reason)

    def test_stage2(self):
        self.assertFalse(self.trig.during_generation([("Stuart Rosenberg", "directed", "Move")]).retrieve)
        d = self.trig.during_generation([("Jean-Daniel Pollet", "born in", "Brazil")])
        self.assertTrue(d.retrieve)
        self.assertEqual(d.query, "Jean-Daniel Pollet born in")


class TestT2RAG(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify(Triplet("a", "p", "b")), "resolved")
        self.assertEqual(classify(Triplet("a", "p", "?x")), "searchable")
        self.assertEqual(classify(Triplet("?x", "p", "?y")), "fuzzy")

    def test_running_example(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("ex4", os.path.join(HERE, "..", "examples", "04_t2rag.py"))
        ex4 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex4)
        pipe = T2RAG(ex4.decompose, HybridRetriever(DOCS).retrieve_text, ex4.resolve, ex4.answer)
        ans, state, log = pipe.run(QUESTION)
        self.assertEqual(ans, GOLD)
        self.assertEqual(len(state.resolved), 4)
        self.assertEqual(max(it for it, _, _ in log), 2)  # 2 hops -> 2 iterations


if __name__ == "__main__":
    unittest.main()
