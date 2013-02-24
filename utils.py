
import re

def n_tuples(tup, tail):
    """
    Grabs a tuple the length of the first argument and shifts into the tail recursively,
    as a recursive sliding window.
    """
    l = [tup]
    if len(tail) > 0:
        next_tup = tuple(tup[1:] + tuple([tail[0]]))
        return l + n_tuples(next_tup, tail[1:])
    else:
        return l + [tuple(tup[1:] + (None,))]

def ngrams(sentence, n=2):
    """Returns n-grams as a list of tuples."""
    if len(sentence) > 0:
        return n_tuples((None,) + tuple(sentence[:n-1]), sentence[n-1:])
    else:
        return []

sentence_splitter_regex = re.compile("[\.;:]\s+")
def text_to_sentences(text):
    """Splits a text string into a list of sentences."""
    lowercase = text.lower()
    raw_sentences = sentence_splitter_regex.split(lowercase)
    stripped_sentences = [s.strip() for s in raw_sentences]
    return stripped_sentences

word_cleaner_regex = re.compile("%s(\w+)%s" % (("\W*",) * 2))
word_filter_regex = re.compile(".*[a-z]+.*")
def sentence_to_words(sentence):
    """Splits a sentence string into a list of words."""
    raw_words = sentence.split()
    cleaned_words = [word_cleaner_regex.sub("\\1", word) for word in raw_words]
    words = filter(lambda x: word_filter_regex.match(x), cleaned_words)
    return words
