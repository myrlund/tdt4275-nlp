########################
# Context-Free Grammar #
########################


mygrammar=(
    """
S -> NP VP
NP -> Det N PP | Det N
VP -> V NP PP | V NP | V
PP -> P NP
NP -> 'I'
Det -> 'the' | 'a'
N -> 'man' | 'park' | 'dog' | 'telescope'
V -> 'ate' | 'saw'
P -> 'in' | 'under' | 'with'
"""
)
