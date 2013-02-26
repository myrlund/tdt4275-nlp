
from collections import Counter, defaultdict
from nltk.corpus import brown

def tag_transition_probabilites(tagged_corpus):
    tuples = []
    tagged_words = tagged_corpus.tagged_words()
    for i in range(len(tagged_words) - 1):
        tuples.append((tagged_words[i][1], tagged_words[i+1][1]))
    
    counted_tags = Counter(tuples)
    counted_tags['_total'] = sum(counted_tags.values())
    return defaultdict(int, counted_tags)

tag_transitions = None
def tag_transition_probability(tag_transition):
    global tag_transitions
    
    if tag_transitions is None:
        tag_transitions = tag_transition_probabilites(brown)
    
    return 1.0 * tag_transitions[tag_transition] / tag_transitions['_total']
