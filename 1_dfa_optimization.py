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






























Let’s practice exactly the kind of thing you’d do in an exam, on paper, using the same theory your `1_dfa_optimization.py` code is based on. We’ll do one full example by hand: regex → syntax tree info → DFA (at least the main states). [reddit](https://www.reddit.com/r/learnprogramming/comments/k7ej1w/how_do_i_solve_coding_exercises_on_paper/)

I’ll use a **small but non-trivial regex** that teachers love:

\[
r = a(b|c)^*
\]

This means: strings that start with `a`, followed by zero or more `b` or `c`.  

In the exam they usually add an end-marker `#` internally, but on paper you can ignore printing `#` unless they explicitly ask for it; we’ll still think about it logically, because your code uses it. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

***

## Step 1: Add explicit concatenation and `#`

In exam solutions (theory), they often show the regex as:

\[
r' = a.(b|c)^*.\#
\]

- Dots mean concatenation.  
- `#` is a special end symbol for direct DFA construction. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

You usually **just write**:  
- `a (b|c)* #` with annotations, or  
- explicitly draw the syntax tree with an end marker leaf.

Question for you after this step: in an exam, would you write dots explicitly, or just mention “we treat concatenation as an operator of precedence between union and star”?

***

## Step 2: Number the leaf positions

Leaves are all symbols from the alphabet plus `#`. For `a(b|c)*#` the leaves are:

- `a`  
- `b`  
- `c`  
- `#`  

Do an in-order traversal and number the leaves as you encounter them (this matches what your code does in `assign_positions`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

One possible numbering:

- position 1: `a`  
- position 2: `b`  
- position 3: `c`  
- position 4: `#`  

On paper you can draw a table:

| pos | symbol |
|-----|--------|
| 1   | a      |
| 2   | b      |
| 3   | c      |
| 4   | #      |

This is what your code stores in `pos_symbol`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

***

## Step 3: Compute nullable, firstpos, lastpos for each subexpression

Do it bottom–up, as in `compute(root)`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

1. **Leaves**:  
   - `a` at position 1:  
     - nullable = False  
     - firstpos = {1}  
     - lastpos = {1}  
   - `b` at position 2:  
     - nullable = False  
     - firstpos = {2}  
     - lastpos = {2}  
   - `c` at position 3:  
     - nullable = False  
     - firstpos = {3}  
     - lastpos = {3}  
   - `#` at position 4:  
     - nullable = False  
     - firstpos = {4}  
     - lastpos = {4}  

2. **Subexpression `b|c`**:  
   - nullable = nullable(b) or nullable(c) = False or False = False  
   - firstpos = {2} ∪ {3} = {2, 3}  
   - lastpos = {2} ∪ {3} = {2, 3}  

3. **Subexpression `(b|c)*`**:  
   - nullable = True (Kleene star is always nullable)  
   - firstpos = firstpos(b|c) = {2, 3}  
   - lastpos = lastpos(b|c) = {2, 3}  

4. **Subexpression `a.(b|c)*`**:  
   - nullable = nullable(a) and nullable((b|c)*)  
   - = False and True = False  
   - firstpos: since left (`a`) is not nullable, firstpos = firstpos(left) = {1}  
   - lastpos: since right is nullable, lastpos = lastpos(left) ∪ lastpos(right) = {1} ∪ {2, 3} = {1, 2, 3}  

5. **Subexpression `a.(b|c)*.#`** (full regex):  
   - nullable = nullable(left) and nullable(#) = False and False = False  
   - firstpos: left is not nullable, so firstpos = firstpos(left) = {1}  
   - lastpos: right is not nullable, so lastpos = lastpos(right) = lastpos(#) = {4}  

This is exactly what your program prints in the node table, but on paper you just show a clean, compact derivation like above. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

***

## Step 4: Compute followpos

Use the rules your code uses: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

- For concatenation `X.Y`:
  - For every `i` in `lastpos(X)`, add `firstpos(Y)` to `followpos(i)`.  
- For star `X*`:
  - For every `i` in `lastpos(X)`, add `firstpos(X)` to `followpos(i)`.  

Apply to this regex:

1. Concatenation `a.(b|c)*`:
   - `lastpos(a)` = {1}  
   - `firstpos((b|c)*)` = {2, 3}  
   - So for `i = 1`, `followpos(1) ⊇ {2, 3}`  

2. Star `(b|c)*`:
   - `lastpos(b|c)` = {2, 3}  
   - `firstpos(b|c)` = {2, 3}  
   - For each `i` in {2, 3}, `followpos(i) ⊇ {2, 3}`  

3. Concatenation `(a.(b|c)*).#`:
   - `lastpos(a.(b|c)*)` = {1, 2, 3}  
   - `firstpos(#)` = {4}  
   - For each `i` in {1, 2, 3}, `followpos(i) ⊇ {4}`  

Combine them:

- `followpos(1)`: from step 1 and step 3  
  - {2, 3} ∪ {4} = {2, 3, 4}  
- `followpos(2)`: from star and last concatenation  
  - {2, 3} ∪ {4} = {2, 3, 4}  
- `followpos(3)`: similarly {2, 3} ∪ {4} = {2, 3, 4}  
- `followpos(4)`: nothing added (end marker).  

On paper, you present a small table:

| pos | symbol | followpos   |
|-----|--------|------------|
| 1   | a      | {2,3,4}    |
| 2   | b      | {2,3,4}    |
| 3   | c      | {2,3,4}    |
| 4   | #      | ∅          |

This matches what your program’s `print_followpos` outputs. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

***

## Step 5: Build DFA states by hand

Use the direct construction rules: start state is `firstpos(root)`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

- Start state \( S_0 = \{1\} \)  

Alphabet = {a, b, c} (ignore `#`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

From each state, for each symbol, you take all positions in that state with that symbol, and union their followpos. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)

1. From state `{1}`:
   - On `a`:  
     - positions with `a` in `{1}`: just 1  
     - next positions = followpos(1) = {2,3,4}  
     - new state: `{2,3,4}`  
   - On `b`: none (no position with symbol b in `{1}`) → dead / no transition.  
   - On `c`: none.  

Call `{2,3,4}` = S1.  

2. From state `{2,3,4}`:
   - On `a`: no positions with `a` here → no transition.  
   - On `b`:  
     - positions with `b`: {2}  
     - followpos(2) = {2,3,4} → state `{2,3,4}` (self-loop on b)  
   - On `c`:  
     - positions with `c`: {3}  
     - followpos(3) = {2,3,4}` → state `{2,3,4}` (self-loop on c)  

Accepting states: those containing position of `#` i.e. 4. So any state that includes 4 is accepting. Here `{2,3,4}` (S1) is accepting.  

Exam-style final DFA:

- States: S0 = {1}, S1 = {2,3,4}.  
- Start state: S0.  
- Final state: S1.  
- Transitions:
  - S0 --a--> S1  
  - S1 --b--> S1  
  - S1 --c--> S1  

This is exactly the intuitive DFA for `a(b|c)*`: accept strings starting with `a`, then any sequence of `b` and `c`. The algorithm matches your program’s `build_dfa` output.  [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/be60f673-c42f-46ae-a5db-5634144a1eda/1_dfa_optimization.py)  

***

In an exam, the marker wants to see these key items:

- Leaf numbering and pos-symbol mapping.  
- Nullable, firstpos, lastpos table for main subexpressions.  
- Followpos table.  
- DFA states and transition diagram (or table), with final states clearly marked.  

To practice: try doing the same full procedure for regex `ab*` (with `#`), and see if you can compute firstpos, lastpos, followpos, and DFA states without looking back. What regex would you like to try next on paper so we can compare your working with the algorithm?
