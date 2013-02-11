#!/usr/bin/env python
# coding: utf8

from corpora import loader
from collections import Counter

import re

def pairs(x1, x2, tail):
    pair = [(x1, x2)]
    if len(tail) > 0:
        return pair + pairs(x2, tail[0], tail[1:])
    else:
        return pair + [(x2, None)]

def sentence_bigrams(sentence): # (None, the), (the, long), (long, white), (white, man), (man, None)
    if len(sentence) > 0:
        return pairs(None, sentence[0], sentence[1:])
    else:
        return []

def filtered_sentences(txt):
    lower = txt.lower()
    s_sentences = re.split("[.,;:]+", lower)
    word = re.compile("[a-z\-]+")
    sentences = [s.split() for s in s_sentences]
    return [filter(lambda x: word.match(x), xs) for xs in sentences]

def words(txt):
    sentences = filtered_sentences(txt)
    flat_words = reduce(lambda acc, xs: acc + xs, sentences, [])
    c = Counter(flat_words)
    c['_total'] = len(flat_words)
    return c

def bigrams(txt):
    sentences = filtered_sentences(txt)
    bigrams = map(sentence_bigrams, sentences)
    flat_bigrams = reduce(lambda acc, xs: acc + xs, bigrams, [])
    c = Counter(flat_bigrams)
    c['_total'] = len(flat_bigrams)
    return c

def unsmoothed_bigram(word, previous_word, words=[], bigrams=[]):
    # P(word|previous_word) = P(previous_word word) / P(previous_word)
    n_bigrams_with_prev = sum([v for k, v in bigrams.iteritems() if k[0] == previous_word])
    n_both =              bigrams.get((previous_word, word), 0)
    
    print n_both, n_bigrams_with_prev
    
    if n_bigrams_with_prev > 0:
        return 1.0 * n_both / n_bigrams_with_prev
    else:
        return None

def most_popular_bigram(word):
    pass

if __name__ == '__main__':
    txt = loader.load_traversed_text()
    bgs = bigrams(txt)
    ws = words(txt)
    print unsmoothed_bigram('course', 'the', ws, bgs)
