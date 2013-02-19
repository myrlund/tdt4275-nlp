#!/usr/bin/env python
# coding: utf8

import hashlib

from loader import *
from word_frequencies import text_to_counted_ngrams

def unsmoothed_unigram(word):
    """Calculates the chance of a word occuring based on its frequency in the corpus."""
    pass

def _unsmoothed_bigram(word, previous_word, words=[], bigrams=[]):
    # P(word|previous_word) = P(previous_word word) / P(previous_word)
    n_bigrams_with_prev = sum([v for k, v in bigrams.iteritems() if k[0] == previous_word])
    n_both =              bigrams.get((previous_word, word), 0)
    
    print n_both, n_bigrams_with_prev
    
    if n_bigrams_with_prev > 0:
        return 1.0 * n_both / n_bigrams_with_prev
    else:
        return None

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(10000)
    corpora = Corpora()
    for n in range(1, 5 + 1):
        corpora.ngrams(n)
    
