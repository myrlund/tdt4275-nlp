
plurality_grammar=(
"""
S -> S_SG | S_PL
S_SG -> NP_SG VP_SG
S_PL -> NP_PL VP_PL
NP -> NP_SG | NP_PL
NP_SG -> Det_SG N_SG NPP
NP_PL -> Det_PL N_PL NPP
NPP -> | PP NPP
VP_SG -> V_SG NP PP | V_SG NP | V_SG
VP_PL -> V_PL NP PP | V_PL NP | V_PL
PP -> P NP
NP_PL -> 'I' | 'you' | 'we' | 'they'
NP_SG -> 'he' | 'she' | 'it'
Det_PL -> 'the' | 'these' | 'those'
Det_SG -> 'a' | 'the'
N_SG -> 'man' | 'park' | 'dog' | 'telescope'
N_PL -> 'dogs' | 'telescopes'
V_PL -> 'eat' | 'see' | 'ate'
V_SG -> 'eats' | 'sees' | 'ate'
P -> 'in' | 'under' | 'with'
"""
)
