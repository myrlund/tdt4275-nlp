import nltk

def part1():
    from cfg import unifying_grammar
    # grammar = nltk.parse_cfg(unifying_grammar)

    parser = nltk.load_parser('file:feat1.fcfg')

    # Give the parser pairs of correct/erronous sentences
    sentences = [
     ("I want to spend lots of money", "me want to spend lots of money"),
     ("tell me about Chez Parnisse", "tell I about Chez Parnisse"),
     ("I would like to take her out to dinner", "I would like to take she out to dinner"),
     ("she does not like Italian", "her does not like Italian"),
    ]

    for pair in sentences:

        for sentence in pair:
            trees = parser.nbest_parse(sentence.split())
            print ("%-40s" % sentence),
            if len(trees) > 0:
                print "OK"
            else:
                print "FAIL"

        print ""

if __name__ == '__main__':
    print "~ Part 1 ~\n"
    part1()
