########################
# Context-Free Grammar #
########################

simple_grammar=(
    """
S -> NP VP
NP -> Det N NPP
NPP -> | PP NPP
VP -> V NP PP | V NP | V
PP -> P NP
NP -> 'I'
Det -> 'the' | 'a'
N -> 'man' | 'park' | 'dog' | 'dogs' | 'telescope'
V -> 'ate' | 'saw' | 'sees'
P -> 'in' | 'under' | 'with'
"""
)
