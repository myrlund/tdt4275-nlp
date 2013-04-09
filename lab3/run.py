import nltk

def get_parser(f, trace):
    return nltk.load_parser(f, trace=trace)

def part1(sentence, debug):
    # grammar = nltk.parse_cfg(unifying_grammar)

    fcfg = 'file:feat1.fcfg'
    trace = 2 if debug else 0
    parser = get_parser(fcfg, trace)

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

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Parses sentences.")
    parser.add_argument('-s', '--sentence', nargs=1, help="single run on a given sentence (default: predefined test set)")
    parser.add_argument('--debug', action='store_true', help="print traces and parse trees.")
    args = parser.parse_args()

    print "~ Part 1 ~\n"
    part1(args.sentence, debug=args.debug)
