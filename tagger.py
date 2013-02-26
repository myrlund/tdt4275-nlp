
from collections import Counter, defaultdict
from nltk.corpus import brown
import operator

tag_counts = None
def counted_tags(tagged_words):
    global tag_counts
    if tag_counts is not None:
        return tag_counts
    
    tag_counts = Counter([tagged_word[1] for tagged_word in tagged_words])
    tag_counts['_total'] = sum(tag_counts.values())
    return tag_counts

tag_transitions = None
def tag_transition_probabilites(tagged_words):
    global tag_transitions
    if tag_transitions is not None:
        return tag_transitions
    
    tuples = []
    for i in range(len(tagged_words) - 1):
        tuples.append((tagged_words[i][1], tagged_words[i+1][1]))
    
    counted_tags = Counter(tuples)
    counted_tags['_total'] = sum(counted_tags.values())
    tag_transitions = defaultdict(int, counted_tags)
    
    return tag_transitions

counted_word_taggings = None
def count_word_taggings(tagged_words):
    global counted_word_taggings
    if counted_word_taggings is not None:
        return counted_word_taggings
    
    counted_word_taggings = Counter(tagged_words)
    return counted_word_taggings

# Task 3a
def simple_most_likely_tag(word):
    word_taggings = count_word_taggings(brown.tagged_words())
    
    filtered_word_taggings = [(t,c) for (t,c) in word_taggings.iteritems() if t[0] == word]
    if len(filtered_word_taggings) > 0:
        sorted_word_taggings = sorted(filtered_word_taggings, key=operator.itemgetter(1))
        return sorted_word_taggings[-1][0][1]
    else:
        return None

def word_probability_given_tag(tag, word):
    counted_word_taggings = count_word_taggings(brown.tagged_words())
    filtered_word_taggings = [(t,c) for (t,c) in counted_word_taggings.iteritems() if t[1] == tag]
    word_tag_count = counted_word_taggings[(word, tag)]
    total_tag_word_count = sum([c for (t,c) in filtered_word_taggings])
    return 1.0 * word_tag_count / total_tag_word_count

def most_relevant_tags(words):
    tags = []
    word_taggings = count_word_taggings(brown.tagged_words())
    
    for word in words:
        filtered_word_taggings = [(t,c) for (t,c) in word_taggings.iteritems() if t[0] == word]
        tags += [tag[1] for (tag,c) in filtered_word_taggings]
    
    return set(tags)

def viterbi(words, tag_probability, tag_transition_probability, word_probability_given_tag):
    V = [{}]
    final_path = {}
    
    tags = most_relevant_tags(words)
    
    # Initialize base cases
    for tag in tags:
        V[0][tag] = tag_probability(tag) * word_probability_given_tag(tag, words[0])
        final_path[tag] = [tag]
    
    # Run viterbi
    for t in range(1, len(words)):
        V.append({})
        path = {}
        
        for tag in tags:
            (probability, _tag) = max([((V[t-1][tag0] * tag_transition_probability((tag0, tag)) * word_probability_given_tag(tag, words[t])), tag0) for tag0 in tags])
            V[t][tag] = probability
            path[tag] = final_path[_tag] + [tag]
        
        final_path = path
    
    (prob, tag) = max([(V[len(words) - 1][tag], tag) for tag in tags])
    
    return (prob, final_path[tag])

def tag_transition_probability(tag_transition):
    tagged_words = brown.tagged_words()
    
    tag_transitions = tag_transition_probabilites(tagged_words)
    tags = counted_tags(tagged_words)
    
    return 1.0 * tag_transitions[tag_transition] / tags[tag_transition[0]]

def tag_probability(tag):
    tag_counts = counted_tags(brown.tagged_words())
    return 1.0 * tag_counts[tag] / tag_counts['_total']

def test_viterbi(sentence):
    print viterbi(sentence.split(), tag_probability, tag_transition_probability, word_probability_given_tag)
