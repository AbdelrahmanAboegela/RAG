"""ragkit: small, dependency-free reference implementations of the ideas in this repo.

These are teaching implementations. They show the mechanism of each paper in a
few dozen lines so you can read, step through, and modify them. They are not the
authors' code and do not reproduce paper numbers. For that, see ../experiments/.
"""

from .metrics import exact_match, f1_score, normalize_answer
from .text import tokenize, chunk_words, chunk_sentences
from .bm25 import BM25
from .dense import HashingEmbedder, DenseIndex, cosine
from .fusion import reciprocal_rank_fusion
from .agentic import parse_action, AgenticRAG, Step
from .autosearch_reward import autosearch_reward, minimal_sufficient_depth
from .quco import CorpusStats, InMemoryCorpusStats, QuCoTrigger
from .t2rag import Triplet, TripletState, classify, T2RAG
from .rrf_hybrid import HybridRetriever
from .rerank import ProximityReranker, mmr, lost_in_the_middle_order
from .graph import TripletGraph
from .rl import group_relative_advantages, masked_policy_loss, token_mask_from_steps
from .cache import GroundedAnswerCache
from .raptor import RaptorTree
from .router import HeuristicRouter
from .evaluate import evaluate, retrieval_metrics, cover_em
from .llm import OpenAICompatibleLLM

__all__ = [
    "ProximityReranker", "mmr", "lost_in_the_middle_order", "TripletGraph",
    "group_relative_advantages", "masked_policy_loss", "token_mask_from_steps",
    "GroundedAnswerCache", "RaptorTree", "HeuristicRouter",
    "evaluate", "retrieval_metrics", "cover_em", "OpenAICompatibleLLM",
    "exact_match", "f1_score", "normalize_answer",
    "tokenize", "chunk_words", "chunk_sentences",
    "BM25", "HashingEmbedder", "DenseIndex", "cosine",
    "reciprocal_rank_fusion", "HybridRetriever",
    "parse_action", "AgenticRAG", "Step",
    "autosearch_reward", "minimal_sufficient_depth",
    "CorpusStats", "InMemoryCorpusStats", "QuCoTrigger",
    "Triplet", "TripletState", "classify", "T2RAG",
]
