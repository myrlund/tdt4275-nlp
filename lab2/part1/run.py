import nltk, sys

def ex1():
    from ex1_cfg import mygrammar
    grammar = nltk.parse_cfg(mygrammar)
    run_grammar(grammar, "the man ate a dog")

def ex2():
    from ex2_cfg import simple_grammar
    grammar = nltk.parse_cfg(simple_grammar)
    run_grammar(grammar, "the man in the park saw a dog with a telescope")

def ex3():
    from ex3_cfg import plurality_grammar
    grammar = nltk.parse_cfg(plurality_grammar)
    run_grammar(grammar, "I sees a dogs")
    run_grammar(grammar, "the man with the telescope ate the dog in a park")

def run_grammar(grammar, input):
    rd_parser = nltk.RecursiveDescentParser(grammar)
    trees = rd_parser.nbest_parse(input.split())

    print "%d trees matches input '%s':" % (len(trees), input)
    for tree in trees:
        print tree

if __name__ == '__main__':
    for i, ex_fn in enumerate((ex1, ex2, ex3)):
        print "Exercise", str(unichr(ord('A') + i))
        ex_fn()
        print ""
