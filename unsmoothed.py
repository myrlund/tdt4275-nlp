#!/usr/bin/env python
# coding: utf8

import hashlib

from loader import *
from word_frequencies import text_to_counted_ngrams

def unsmoothed_ngram(corpora, word, preceding=[], good_turing=False):
    """Calculates the chance of a word occuring based on its frequency in the corpus."""
    n = len(preceding) + 1
    if n > 2:
        print "Supports only uni- and bi-grams."
        return None
    
    unigrams = corpora.ngrams(1)
    if n == 1:
        return 1.0 * unigrams[word] / unigrams['_total']
    else:
        bigrams = corpora.ngrams(n)
        bigram = tuple(preceding) + (word,)
        return 1.0 * bigrams[bigram] / unigrams[tuple(preceding)]
        
Corpora.unsmoothed_ngram = unsmoothed_ngram

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
    import argparse, sys
    
    sys.setrecursionlimit(10000)
    corpora = Corpora()
    
    parser = argparse.ArgumentParser(description="Computes unsmoothed bigrams.")
    parser.add_argument('-g', '--good-turing', action='store_true', help="Use good-turing discounting.")
    parser.add_argument('words', nargs='+')
    args = parser.parse_args()
    
    print corpora.unsmoothed_ngram(args.words[-1], preceding=tuple(args.words[:-1]), good_turing=args.good_turing)
    
    