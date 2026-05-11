# Left Recursion Removal + FIRST and FOLLOW

grammar = {}

n = int(input("Enter number of productions: "))

print("Enter productions:")

# ---------------- INPUT ----------------

for i in range(n):

    rule = input()

    left, right = rule.split("->")

    grammar[left] = right.split("|")


# ---------------- TOKENIZE ----------------

def tokenize(prod):

    tokens = []
    i = 0

    while i < len(prod):

        if i + 1 < len(prod) and prod[i + 1] == "'":
            tokens.append(prod[i] + "'")
            i += 2

        else:
            tokens.append(prod[i])
            i += 1

    return tokens


# ---------------- REMOVE LEFT RECURSION ----------------

new_grammar = {}

for nt in grammar:

    alpha = []
    beta = []

    for prod in grammar[nt]:

        tokens = tokenize(prod)

        if tokens[0] == nt:
            alpha.append(tokens[1:])

        else:
            beta.append(tokens)

    if alpha:

        new_nt = nt + "'"

        new_grammar[nt] = []

        for b in beta:
            new_grammar[nt].append(b + [new_nt])

        new_grammar[new_nt] = []

        for a in alpha:
            new_grammar[new_nt].append(a + [new_nt])

        new_grammar[new_nt].append(['e'])

    else:
        new_grammar[nt] = [tokenize(p) for p in grammar[nt]]


# ---------------- PRINT NEW GRAMMAR ----------------

print("\nAfter removing Left Recursion:\n")

for nt in new_grammar:

    rhs = []

    for prod in new_grammar[nt]:
        rhs.append("".join(prod))

    print(nt, "->", " | ".join(rhs))


# ---------------- FIRST ----------------

first = {}

for nt in new_grammar:
    first[nt] = set()


def find_first(symbol):

    # terminal
    if symbol not in new_grammar:
        return {symbol}

    if len(first[symbol]) != 0:
        return first[symbol]

    for prod in new_grammar[symbol]:

        if prod[0] == 'e':
            first[symbol].add('e')

        else:

            for sym in prod:

                temp = find_first(sym)

                first[symbol].update(temp - {'e'})

                if 'e' not in temp:
                    break

            else:
                first[symbol].add('e')

    return first[symbol]


for nt in new_grammar:
    find_first(nt)


# ---------------- FOLLOW ----------------

follow = {}

for nt in new_grammar:
    follow[nt] = set()

start_symbol = list(new_grammar.keys())[0]

follow[start_symbol].add('$')


changed = True

while changed:

    changed = False

    for head in new_grammar:

        for prod in new_grammar[head]:

            for i in range(len(prod)):

                B = prod[i]

                if B in new_grammar:

                    # beta exists
                    if i + 1 < len(prod):

                        beta = prod[i + 1]

                        before = len(follow[B])

                        if beta in new_grammar:

                            follow[B].update(first[beta] - {'e'})

                            if 'e' in first[beta]:
                                follow[B].update(follow[head])

                        else:
                            follow[B].add(beta)

                        if len(follow[B]) > before:
                            changed = True

                    else:

                        before = len(follow[B])

                        follow[B].update(follow[head])

                        if len(follow[B]) > before:
                            changed = True


# ---------------- PRINT TABLE ----------------

print("\n---------------------------------------------")
print("NT\tFIRST\t\tFOLLOW")
print("---------------------------------------------")

for nt in new_grammar:

    print(nt,
          "\t",
          first[nt],
          "\t",
          follow[nt])