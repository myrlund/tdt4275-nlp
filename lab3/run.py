import nltk

def get_parser(f, debug):
    trace = 2 if debug else 0
    return nltk.load_parser(f, trace=trace)

def part1a(sentence, debug):
    # grammar = nltk.parse_cfg(unifying_grammar)

    fcfg = 'file:feat1.fcfg'
    parser = get_parser(fcfg, debug)

    # Give the parser pairs of correct/erronous sentences
    if sentence:
        sentences = [sentence]
    else:
        sentences = [
         ("I want to spend lots of money", "me want to spend lots of money"),
         ("tell me about Chez Parnisse", "tell I about Chez Parnisse"),
         ("I would like to take her out to dinner", "I would like to take she out to dinner"),
         ("she does not like Italian", "her does not like Italian"),
         ("this dog runs", "I runs", "these dogs runs"),
        ]

    # Run them through the parser and display either OK or FAIL
    for pair in sentences:
        for sentence in pair:
            trees = parser.nbest_parse(sentence.split())
            print ("%-40s" % sentence),
            if len(trees) > 0:
                print "OK"
            else:
                print "FAIL"

            if debug:
                for tree in trees:
                    print tree
        print ""

def part1b(debug):
    lp = nltk.LogicParser()

    logic = [
        "all x y.(Shark(x) & Bird(y) & -Eats(x, y))",
        "-(all x.(Bird(x) & LaysEggs(x)))",
    ]
    for l in logic:
        print "Parsing: '%s'" % l

        parsed_logic = lp.parse(l)
        print " -> free variables: %s" % parsed_logic.free()
        print ""

def part1c(debug):
    lp = nltk.LogicParser()
    a3 = lp.parse('exists x.(samfundet(x) and school(x))')
    c1 = lp.parse('smart(jonas)')
    c2 = lp.parse('-smart(jonas)')

    mace = nltk.Mace()
    print mace.build_model(None, [a3, c1])
    print mace.build_model(None, [a3, c2])
    print mace.build_model(None, [c1, c2])


def part2a(sentence, debug):
    fcfg = "file:fragment.fcfg"
    # parser = get_parser(fcfg, debug)

    if not sentence:
        sentence = "a man chases a dog"

    print "Parsing: '%s'" % sentence
    trace = 2 if debug else 0
    results = nltk.batch_interpret([sentence], fcfg, trace=trace)
    for result in results:
        for (synrep, semrep) in result:
            print synrep
            print semrep

if __name__ == '__main__':
    parts = {
        '1a': part1a,
        '1b': part1b,
        '1c': part1c,
        '2a': part2a,
    }

    import argparse
    parser = argparse.ArgumentParser(description="Parses sentences.")
    parser.add_argument('-s', '--sentence', nargs=1, help="single run on a given sentence (default: predefined test set)")
    parser.add_argument('--parts', nargs='+', help="run only the specified parts (choose from %s)" % ", ".join(sorted(parts.keys())))
    parser.add_argument('--skip', nargs='*', help="do not run the specified parts (choose from %s)" % ", ".join(sorted(parts.keys())))
    parser.add_argument('--debug', action='store_true', help="print traces and parse trees")

    args = parser.parse_args()

    run_parts = set(args.parts or parts.keys()) - set(args.skip or [])

    # Part 1
    if '1a' in run_parts: parts['1a'](args.sentence, debug=args.debug)
    if '1b' in run_parts: parts['1b'](debug=args.debug)
    if '1c' in run_parts: parts['1c'](debug=args.debug)
    if '2a' in run_parts: parts['2a'](args.sentence[0] if args.sentence else None, debug=args.debug)
