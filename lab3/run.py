import nltk

def part1():
    from cfg import unifying_grammar
    # grammar = nltk.parse_cfg(unifying_grammar)

    parser = nltk.load_parser('file:feat1.fcfg', trace=2)

    i = "I want to spend lots of money"
    trees = parser.nbest_parse(i.split())

    for tree in trees:
        print tree

    print ""

if __name__ == '__main__':
    part1()
