"""A tiny corpus built around the running example used throughout the docs.

Running example (a 2WikiMultihopQA-style comparison question, also the example
in the State-Aware RAG paper's Figure 1):

    "Are the directors of Move (1970) and Méditerranée (1963) from the same country?"

Answering needs 4 hops: director of each film, then nationality of each director.
Distractor passages are included on purpose (same surname, same year, a
different film called 'Move') so that naive top-k retrieval gets noisy.
"""

QUESTION = "Are the directors of Move (1970) and Méditerranée (1963) from the same country?"
GOLD = "no"

DOCS = [
    "Move (1970 film). Move is a 1970 American comedy film directed by Stuart Rosenberg and starring Elliott Gould.",
    "Stuart Rosenberg was an American film and television director, known for Cool Hand Luke. He was born in New York City.",
    "Méditerranée (1963 film). Méditerranée is a 1963 French experimental short film directed by Jean-Daniel Pollet.",
    "Jean-Daniel Pollet was a French filmmaker and screenwriter associated with the French New Wave.",
    "Move (2020 series). Move is a Netflix documentary series about dance and choreography.",
    "Rosenberg is a surname. Notable people include Ethel Rosenberg and Julius Rosenberg.",
    "Cool Hand Luke is a 1967 American prison drama film starring Paul Newman.",
    "The French New Wave was a film movement that emerged in France in the late 1950s.",
    "Elliott Gould is an American actor who starred in M*A*S*H and The Long Goodbye.",
    "In 1963 several experimental films premiered at European festivals.",
]
