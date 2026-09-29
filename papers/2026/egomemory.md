# EgoMemory: Memory-Augmented Personalized Retrieval for Long-Context Egocentric Video

| | |
|---|---|
| **Authors** | Yuanmin Tang, Jue Zhang, Xiaoting Qin, Jing Yu, Meikang Qiu, Gaopeng Gou, Gang Xiong, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, Qi Wu |
| **Venue / status** | **Findings of ACL 2026** |
| **Links** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.362/) · code: not linked |
| **Section** | 6, Memory and state (multimodal, personal) |
| **Verified** | Anthology abstract (September 2026) |

**Task.** Personalised **episodic memory retrieval** from first-person (egocentric) video: "Where did I leave *my* blue mug?"

**Benchmark.** 165,795 user-specific object annotations over 245 videos from 45 participants, with 639 human-curated queries.

**Method.** **EgoRetriever** is *training-free*: an MLLM combined with **reflective chain-of-thought** prompting that reasons about which moments in a long video are relevant to a personalised query.

**Results.** It beats baselines on EgoMemory, EgoCVR and EgoLife.

**Why it matters.** It pushes RAG toward **personal, multimodal, lifelong memory**, where the "corpus" is the user's own life and relevance depends on who is asking.
