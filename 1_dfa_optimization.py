# DFA Optimization Program
# Input : Regular Expression
# Output: nullable, firstpos, lastpos, followpos and DFA table

from collections import defaultdict

# ---------------- NODE ----------------
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

        self.position = None


# ---------------- GLOBALS ----------------
position = 1
followpos = defaultdict(set)
pos_symbol = {}
all_nodes = []


# ---------------- POSTFIX CONVERSION ----------------
def precedence(op):
    if op == '*':
        return 3
    if op == '.':
        return 2
    if op == '|':
        return 1
    return 0


def infix_to_postfix(regex):
    stack = []
    output = ""

    for ch in regex:

        if ch.isalnum() or ch == '#':
            output += ch

        elif ch == '(':
            stack.append(ch)

        elif ch == ')':
            while stack[-1] != '(':
                output += stack.pop()
            stack.pop()

        else:
            while stack and stack[-1] != '(' and precedence(stack[-1]) >= precedence(ch):
                output += stack.pop()

            stack.append(ch)

    while stack:
        output += stack.pop()

    return output


# ---------------- BUILD TREE ----------------
def build_tree(postfix):

    stack = []

    for ch in postfix:

        node = Node(ch)

        if ch == '*':
            node.left = stack.pop()

        elif ch in ['.', '|']:
            node.right = stack.pop()
            node.left = stack.pop()

        stack.append(node)

    return stack.pop()


# ---------------- NUMBER LEAF NODES ----------------
def assign_positions(root):
    global position

    if root is None:
        return

    assign_positions(root.left)
    assign_positions(root.right)

    if root.left is None and root.right is None:

        root.position = position

        root.firstpos.add(position)
        root.lastpos.add(position)

        pos_symbol[position] = root.value

        position += 1

    all_nodes.append(root)


# ---------------- COMPUTE FUNCTIONS ----------------
def compute(root):

    if root is None:
        return

    compute(root.left)
    compute(root.right)

    # OR operator
    if root.value == '|':

        root.nullable = root.left.nullable or root.right.nullable

        root.firstpos = root.left.firstpos | root.right.firstpos
        root.lastpos = root.left.lastpos | root.right.lastpos

    # CONCAT operator
    elif root.value == '.':

        root.nullable = root.left.nullable and root.right.nullable

        if root.left.nullable:
            root.firstpos = root.left.firstpos | root.right.firstpos
        else:
            root.firstpos = root.left.firstpos

        if root.right.nullable:
            root.lastpos = root.left.lastpos | root.right.lastpos
        else:
            root.lastpos = root.right.lastpos

        for i in root.left.lastpos:
            followpos[i].update(root.right.firstpos)

    # STAR operator
    elif root.value == '*':

        root.nullable = True

        root.firstpos = root.left.firstpos
        root.lastpos = root.left.lastpos

        for i in root.lastpos:
            followpos[i].update(root.firstpos)


# ---------------- PRINT NODE TABLE ----------------
def print_node_table():

    print("\nNODE TABLE")
    print("Node\tNullable\tFirstpos\tLastpos")

    for node in all_nodes:
        print(node.value,
              "\t", node.nullable,
              "\t\t", node.firstpos,
              "\t", node.lastpos)


# ---------------- PRINT FOLLOWPOS ----------------
def print_followpos():

    print("\nFOLLOWPOS TABLE")
    print("Position\tSymbol\tFollowpos")

    for pos in pos_symbol:
        print(pos,
              "\t\t", pos_symbol[pos],
              "\t", followpos[pos])


# ---------------- BUILD DFA ----------------
def build_dfa(root):

    alphabet = set()

    for p in pos_symbol:
        if pos_symbol[p] != '#':
            alphabet.add(pos_symbol[p])

    states = []
    dfa = {}

    start = frozenset(root.firstpos)

    states.append(start)

    i = 0

    while i < len(states):

        current = states[i]
        dfa[current] = {}

        for symbol in alphabet:

            new_state = set()

            for p in current:

                if pos_symbol[p] == symbol:
                    new_state.update(followpos[p])

            new_state = frozenset(new_state)

            if new_state:

                dfa[current][symbol] = new_state

                if new_state not in states:
                    states.append(new_state)

        i += 1

    return states, dfa, alphabet


# ---------------- PRINT DFA TABLE ----------------
def print_dfa(states, dfa, alphabet):

    print("\nDFA TRANSITION TABLE")

    print("State\t", end="")

    for a in alphabet:
        print(a, "\t", end="")

    print()

    state_names = {}

    for i, s in enumerate(states):
        state_names[s] = "S" + str(i)

    for s in states:

        print(state_names[s], "\t", end="")

        for a in alphabet:

            if a in dfa[s]:
                print(state_names[dfa[s][a]], "\t", end="")

            else:
                print("-\t", end="")

        print()


# ---------------- MAIN ----------------
regex = input("Enter Regular Expression: ")

regex = regex + "#"

# Add concatenation operator '.'
new_regex = ""

for i in range(len(regex)):

    new_regex += regex[i]

    if i + 1 < len(regex):

        a = regex[i]
        b = regex[i + 1]

        if (a.isalnum() or a in ['*', ')', '#']) and (b.isalnum() or b == '(' or b == '#'):

            new_regex += '.'

postfix = infix_to_postfix(new_regex)

root = build_tree(postfix)

assign_positions(root)

compute(root)

print_node_table()

print_followpos()

states, dfa, alphabet = build_dfa(root)

print_dfa(states, dfa, alphabet)