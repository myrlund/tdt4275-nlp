#!/usr/bin/env python
# coding: utf8

import hashlib

from loader import *
from operator import mul
from word_frequencies import text_to_counted_ngrams

def unsmoothed_unigram(corpora, words):
    unigrams = corpora.ngrams(1)
    probabilities = [1.0 * unigrams[(word,)] / unigrams['_total'] for word in words]
    return reduce(mul, probabilities, 1)

def unsmoothed_ngram(corpora, words, n=2, sentence=False, good_turing=False):
    """Calculates the chance of a word occuring based on its frequency in the corpus."""
    
    if len(words) < 1 or n < 1:
        return None
    
    if n == 1 or len(words) == 1:
        return unsmoothed_unigram(corpora, words)
    
    ngrams = {}
    ngrams[n] = corpora.ngrams(n)
    ngrams[n-1] = corpora.ngrams(n-1)
    
    if sentence:
        sentence = [None] + words + [None]
    else:
        sentence = words
    
    probabilities = []
    for i in range(len(sentence)-n+1):
        ngram = tuple(sentence[i:i+n])
        p = 1.0 * ngrams[n][ngram] / ngrams[n-1][ngram[:-1]]
        probabilities.append(p)
    
    return reduce(mul, probabilities, 1)
    
Corpora.unsmoothed_ngram = unsmoothed_ngram

if __name__ == '__main__':
    import argparse, sys
    
    sys.setrecursionlimit(10000)
    corpora = Corpora()
    
    parser = argparse.ArgumentParser(description="Computes unsmoothed bigrams.")
    parser.add_argument('-g', '--good-turing', action='store_true', help="Use good-turing discounting.")
    parser.add_argument('-n', type=int, nargs='?', default=2, help="Puts the n in n-gram.")
    parser.add_argument('-s', '--sentence', action='store_true', help="Includes start and end of sentence to the probability calculation.")
    parser.add_argument('words', nargs='+')
    args = parser.parse_args()
    
    print corpora.unsmoothed_ngram(args.words, n=args.n, sentence=args.sentence, good_turing=args.good_turing)
