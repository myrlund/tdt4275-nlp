import nltk

def cky(words, grammar):
    table = dict((i, {}) for i in range(len(words)))

    for j in range(len(words)):

        # Fill inn the POS of each word
        table[j][j + 1] = []
        table[j][j + 1].append([p.lhs() for p in grammar.productions(rhs=words[j])])
        print j

        for i in range(j - 1, -1, -1):
            print j, i
            table[i][j + 1] = []

            for k in range(i + 1, j):
                print j, i, k
                _a = table[i][k]
                _b = table[k][j]

                ps = [(a[0], b[0]) for a in _a for b in _b]
                for p in ps:
                    print grammar.productions(rhs=p)
                # table[j][i] += []

    print table

if __name__ == '__main__':
    from part2_cfg import simple_grammar
    grammar = nltk.parse_cfg(simple_grammar)
    cky("the man saw the dog in the park".split(), grammar)
