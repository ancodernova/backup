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


































Let’s take a **FIRST/FOLLOW + left recursion** sample question like you’d get in a compiler design exam and solve it step by step, by hand, matching the logic in `3_first_follow.py`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

***

## Sample question (exam-style)

**Question:**  
Given the grammar:

\[
S \to S a \mid b
\]

1. Remove immediate left recursion.  
2. Compute FIRST(S) and FOLLOW(S).  

***

## Step 1: Identify left recursion

Production: \( S \to S a \mid b \)

- Left-hand side: S  
- Right-hand side alternatives:
  - `Sa` → starts with S → left-recursive.  
  - `b` → starts with terminal b → non-left-recursive.  

So we are in the pattern \( A \to A\alpha \mid \beta \). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

***

## Step 2: Apply left recursion removal

General pattern:  
If \( A \to A\alpha_1 \mid A\alpha_2 \mid \dots \mid \beta_1 \mid \beta_2 \dots \)  

Transform to:

\[
A \to \beta_1 A' \mid \beta_2 A' \dots
\]
\[
A' \to \alpha_1 A' \mid \alpha_2 A' \mid \dots \mid e
\]

Here:

- A = S  
- Left-recursive part `Sa` ⇒ α = `a`  
- Non-left-recursive part β = `b`  

So new grammar:

- \( S \to b S' \)  
- \( S' \to a S' \mid e \)  

That’s exactly what `new_grammar` in your code would construct: S with productions `bS'`, S' with `aS'` and `e`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

***

## Step 3: Compute FIRST sets

We need FIRST(S) and FIRST(S'). Use standard rules, same as `find_first` in the code. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

1. FIRST of terminals:
   - FIRST(b) = { b }  
   - FIRST(a) = { a }  

2. FIRST(S):
   - S → b S'  
   - First symbol is terminal b, so FIRST(S) = { b }.  

3. FIRST(S'):
   - S' → a S' | e  
   - From `a S'` we get `a`.  
   - From `e` we get `e`.  
   - So FIRST(S') = { a, e }.  

**Answer so far:**

- FIRST(S) = { b }  
- FIRST(S') = { a, e }  

***

## Step 4: Compute FOLLOW sets

Use rules like in the `FOLLOW` loop in the code. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

1. Start symbol: S  
   - Add `$` to FOLLOW(S).  

So initially:

- FOLLOW(S) = { `$` }  
- FOLLOW(S') = { }  

2. Look at each production.

### Production 1: \( S \to b S' \)

- Here S' appears at the **end** of the RHS.  
- Rule: if non-terminal B appears at end of A → add FOLLOW(A) to FOLLOW(B).  
- So FOLLOW(S') includes FOLLOW(S).  

Thus:

- FOLLOW(S') = { `$` }  

### Production 2: \( S' \to a S' \)

- RHS: `a S'`.  
- S' is at the end again, so FOLLOW(S') includes FOLLOW(S'). That adds nothing new.  

No more changes, so:

- FOLLOW(S) = { `$` }  
- FOLLOW(S') = { `$` }  

***

## Final exam-style answers

**1. Grammar without left recursion:**

\[
S \to b S'
\]
\[
S' \to a S' \mid e
\]

**2. FIRST sets:**

- FIRST(S) = { b }  
- FIRST(S') = { a, e }  

**3. FOLLOW sets:**

- FOLLOW(S) = { `$` }  
- FOLLOW(S') = { `$` }  

This is exactly what your `3_first_follow.py` would print if you enter the original grammar and run it. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/4111ef1d-7e21-4627-b11b-1e37f0c154dc/3_first_follow.py)

***

Your turn: can you now try the same procedure for this grammar and see if you can reach FIRST and FOLLOW?  
\[
E \to E+T \mid T
\]  
\[
T \to i
\]  
Briefly outline how you’d remove left recursion from E and what FIRST(E) and FOLLOW(E) would be.
