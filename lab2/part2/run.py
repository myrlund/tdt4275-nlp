import nltk

def ex_a():
    from part2_cfg import simple_grammar
    grammar = nltk.parse_cfg(simple_grammar)

    parsers = (nltk.RecursiveDescentParser,
               nltk.ShiftReduceParser,
               nltk.EarleyChartParser,
               nltk.BottomUpChartParser)

    for parser_class in parsers:
        print "Testing parser:", parser_class.__name__
        parser = parser_class(grammar, trace=2)

        i = "a man saw a man with a cat"
        trees = parser.nbest_parse(i.split())

        print "\n%d trees matches input '%s':" % (len(trees), i)
        for tree in trees:
            print tree

        print ""

def ex_b():
    pass

if __name__ == '__main__':
    for i, fn in enumerate((ex_a, ex_b)):
        print "Exercise", str(unichr(ord('A')+i))
        fn()
        print ""
