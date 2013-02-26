#!/usr/bin/env python

import operator

from collections import Counter, defaultdict
from nltk.corpus import brown

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
def simple_most_likely_tag(word, tagged_words):
    word_taggings = count_word_taggings(tagged_words)
    
    filtered_word_taggings = [(t,c) for (t,c) in word_taggings.iteritems() if t[0] == word]
    if len(filtered_word_taggings) > 0:
        sorted_word_taggings = sorted(filtered_word_taggings, key=operator.itemgetter(1))
        return sorted_word_taggings[-1][0][1]
    else:
        return None

def word_probability_given_tag(tag, word, tagged_words):
    counted_word_taggings = count_word_taggings(tagged_words)
    filtered_word_taggings = [(t,c) for (t,c) in counted_word_taggings.iteritems() if t[1] == tag]
    word_tag_count = counted_word_taggings[(word, tag)]
    total_tag_word_count = sum([c for (t,c) in filtered_word_taggings])
    return 1.0 * word_tag_count / total_tag_word_count

def most_relevant_tags(words, tagged_words):
    tags = []
    word_taggings = count_word_taggings(tagged_words)
    # print word_taggings
    
    for word in words:
        filtered_word_taggings = [(t,c) for (t,c) in word_taggings.iteritems() if t[0] == word]
        # print filtered_word_taggings
        total = sum([c for (tag,c) in filtered_word_taggings])
        tags += [tag[1] for (tag,c) in filtered_word_taggings if c >= total / 3.0]
    
    return set(tags)

def viterbi(words, tag_probability, tag_transition_probability, word_probability_given_tag, tagged_words=None):
    V = [{}]
    final_path = {}
    
    tags = most_relevant_tags(words, tagged_words)
    # print tags
    
    # Initialize base cases
    # print "Fucking base cases."
    for tag in tags:
        V[0][tag] = tag_probability(tag) * word_probability_given_tag(tag, words[0], tagged_words)
        final_path[tag] = [tag]
    # print "Base cases done, starting fucking iterations over the rest."
    
    # Run viterbi
    for t in range(1, len(words)):
        # print " - M" + "oo" * t
        V.append({})
        path = {}
        
        for tag in tags:
            (probability, _tag) = max([((V[t-1][tag0] * tag_transition_probability((tag0, tag), tagged_words) * word_probability_given_tag(tag, words[t], tagged_words)), tag0) for tag0 in tags])
            V[t][tag] = probability
            path[tag] = final_path[_tag] + [tag]
        
        final_path = path
    
    # print words
    # print V
    (prob, tag) = max([(V[len(words) - 1][tag], tag) for tag in tags])
    
    print "Final path:", final_path[tag]
    return zip(words, final_path[tag])

def tag_transition_probability(tag_transition, tagged_words):
    tag_transitions = tag_transition_probabilites(tagged_words)
    tags = counted_tags(tagged_words)
    
    return 1.0 * tag_transitions[tag_transition] / tags[tag_transition[0]]

def tag_probability(tag):
    tag_counts = counted_tags(brown.tagged_words())
    return 1.0 * tag_counts[tag] / tag_counts['_total']

def test_viterbi(sentence):
    print viterbi(sentence.split(), tag_probability, tag_transition_probability, word_probability_given_tag, tagged_words=brown.tagged_words())

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Tags sentences. Yeah.")
    parser.add_argument('-s', '--sentence', nargs=1, help="Single run on a given sentence.")
    parser.add_argument('--test', action='store_true', help="Run tagger on a test set.")
    args = parser.parse_args()
    
    if args.test:
        all_tagged_words = brown.tagged_words()
        
        test_set_size = 1.0/9
        training_set = all_tagged_words[:int(len(all_tagged_words)*test_set_size)]
        test_set = brown.tagged_sents()[int(len(brown.tagged_sents())*test_set_size):]
        
        correct = 0
        total = 0
        
        for sentence in test_set:
            # print "Test set size: %i" % len(sentence)
            result = viterbi([word for (word, tag) in sentence], tag_probability, tag_transition_probability, word_probability_given_tag, tagged_words=training_set)
            for i in range(len(result)):
                if sentence[i][1] == result[i][1]:
                    correct += 1
                    print "."
                else:
                    print "x"
                
                total += 1
                
        print "Got %i of %i right. That's %.2f%." % (correct, total, 1.0 * correct / total)
    else:
        sentence = args.sentence[0]
    
        words = sentence.replace('.', ' .').replace(',', ' ,').split()
        
        print viterbi(words, tag_probability, tag_transition_probability, word_probability_given_tag, tagged_words=brown.tagged_words())
