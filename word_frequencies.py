from itertools import chain
from collections import Counter

from utils import *

def text_to_ngrams(text, n=2):
    """Takes a text and returns an array of n-tuples."""
    sentences = text_to_sentences(text)
    nested_words = [sentence_to_words(sentence) for sentence in sentences]
    nested_ngrams = [ngrams(words, n=n) for words in nested_words]
    return list(chain.from_iterable(nested_ngrams))

def counted_ngrams(ngrams):
    """
    Counts n-grams, and returns them on the form of {(w1, w2, ...): count}.
    Includes a "_total" key with the sum of the values, for convenience.
    """
    c = Counter(ngrams)
    c['_total'] = len(ngrams)
    return c

def text_to_counted_ngrams(text, n=2):
    """Takes a text string and returns a hash like {(w1, w2, ...): count}."""
    ngrams = text_to_ngrams(text, n=n)
    return counted_ngrams(ngrams)
