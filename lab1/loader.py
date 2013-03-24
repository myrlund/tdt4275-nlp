import os, hashlib, pickle

from itertools import chain

from word_frequencies import text_to_counted_ngrams, sentences_to_ngrams, counted_ngrams
from collections import Counter, defaultdict

class Corpus:
    COMPILATION_FORMAT = os.path.join("corpora", "compiled", "%s-%s-%i.nlpc")
    
    filename = None
    data = False
    def __init__(self, filename):
        self.filename = filename
    
    @property
    def text(self):
        t = None
        try:
            with open(self.filename) as f:
                t = f.read()
                f.close()
        except IOError:
            pass
        return t
    
    def compiled_ngram_filename(self, ngram):
        fn = os.path.split(self.filename)[-1]
        md5hash = hashlib.md5(self.text).hexdigest()
        compiled_filename = self.COMPILATION_FORMAT % (fn, md5hash, ngram)
        return compiled_filename
    
    def is_compiled(self, ngram):
        """
        Checks if ngram is compiled.
        Format: $filename-$n-$md5hash
        """
        compiled_filename = self.compiled_ngram_filename(ngram)
        return os.path.isfile(compiled_filename)
    
    def save(self, n, data):
        """Saves a compiled set of n-grams."""
        compiled_filename = self.compiled_ngram_filename(n)
        pickle.dump(data, open(compiled_filename, 'w'))
        self.data = data
    
    def load(self, n):
        """Loads a saved set of n-grams."""
        if self.data:
            return self.data
        else:
            self.data = pickle.load(open(self.compiled_ngram_filename(n)))
            return self.data
    
    def compile_ngrams(self, n):
        counted_ngrams = text_to_counted_ngrams(self.text, n=n)
        return counted_ngrams
    
    def ngrams(self, n):
        if self.is_compiled(n):
            return self.load(n)
        
        print "Cache miss -- recompiling."
        counted_ngrams = self.compile_ngrams(n)
        self.save(n, counted_ngrams)
        return counted_ngrams

class BrownCorpus(Corpus):
    def __init__(self):
        pass
    
    def compiled_ngram_filename(self, ngram):
        return "brown-compiled-%i.nlpc" % ngram
    
    def compile_ngrams(self, n):
        from nltk.corpus import brown
        sentences = brown.sents()
        ngrams = sentences_to_ngrams(sentences, n=n)
        return counted_ngrams(ngrams)

class Corpora:
    corpora = []
    default_corpora = [
     # Corpus('corpora/tabloid/vg.txt'),
     # Corpus('corpora/traversed/all2.txt'),
     # Corpus('corpora/traversed/nyt.txt'),
     BrownCorpus(),
    ]
    
    def __init__(self, corpora=None):
        if corpora is None:
            corpora = Corpora.default_corpora
        
        # Add given corpora
        [self.add_corpus(corpus) for corpus in corpora]
    
    def add_corpus(self, corpus):
        self.corpora.append(corpus)
    
    def ngrams(self, n):
        
        # The defaultdict returns 0 if key doesn't exist
        all_ngrams = defaultdict(int, self.corpora[0].ngrams(n))
        
        # Merge the corpora, summing their values
        for corpus in self.corpora[1:]:
            for k, v in corpus.ngrams(n).iteritems():
                all_ngrams[k] += v
        
        return all_ngrams


