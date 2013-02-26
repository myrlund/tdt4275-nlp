#!/usr/bin/env python
# coding: utf8

import random, operator

from loader import *

def sentence_gen(corpora, priority, length=15):
    """Generates a sentence of given length, based on popular n-grams."""
    ns = range(3, 5 + 1)
    
    counted_ngrams = {}
    sorted_ngrams = {}
    for n in ns:
        counted_ngrams[n] = corpora.ngrams(n)
        sorted_ngrams[n] = sorted(counted_ngrams[n].iteritems(), key=operator.itemgetter(1))[::-1]
    
    words = [None]
    while len(filter(lambda w: w is not None, words)) < length:
        n = ns[random.randint(0, len(ns)-1)]
        ngrams = sorted_ngrams[n]
        
        index = random.randint(priority, priority+2)
        
        filtered_ngrams = filter(lambda k: k[0][0] == words[-1], sorted_ngrams[n])
        if len(words) + n >= length:
            filtered_ngrams = filter(lambda item: item[0][-1] is None, filtered_ngrams)
        
        if filtered_ngrams:
            ngram = filtered_ngrams[min(index, len(filtered_ngrams)-1)]
            ngram_words = ngram[0][1:]
                
            words += ngram_words
        else:
            ngram = sorted_ngrams[n][index]
            words += ["."] + list(ngram[0])
    
    words = filter(lambda w: w is not None, words)
    
    return " ".join(words)

Corpora.sentence_gen = sentence_gen

if __name__ == '__main__':
    corpora = Corpora()
    
    import argparse
    parser = argparse.ArgumentParser(description="Makes silly sentences.")
    parser.add_argument('-n', type=int, nargs='?', default=5, help="How many sentences?")
    parser.add_argument('-l', '--length', type=int, nargs='?', default=15, help="How long sentences?")
    args = parser.parse_args()
    
    for i in range(args.n):
        print corpora.sentence_gen(i, length=args.length)
