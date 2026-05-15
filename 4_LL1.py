# LL(1) Predictive Parser

# Grammar:
# E -> TA
# A -> +TA | e
# T -> FB
# B -> *FB | e
# F -> (E) | i


# ---------------- PARSING TABLE ----------------

table = {

    ('E', 'i'): 'TA',
    ('E', '('): 'TA',

    ('A', '+'): '+TA',
    ('A', ')'): 'e',
    ('A', '$'): 'e',

    ('T', 'i'): 'FB',
    ('T', '('): 'FB',

    ('B', '+'): 'e',
    ('B', '*'): '*FB',
    ('B', ')'): 'e',
    ('B', '$'): 'e',

    ('F', 'i'): 'i',
    ('F', '('): '(E)'
}


# ---------------- CHECK NON TERMINAL ----------------

def is_non_terminal(ch):
    return ch.isupper()


# ---------------- PRINT GRAMMAR ----------------

print("\nGrammar Used:\n")

print("E -> TA")
print("A -> +TA | e")
print("T -> FB")
print("B -> *FB | e")
print("F -> (E) | i")


# ---------------- INPUT ----------------

input_string = input("\nEnter input string: ")

if input_string[-1] != '$':
    input_string += '$'


# ---------------- STACK ----------------

stack = []

stack.append('$')
stack.append('E')

pointer = 0


# ---------------- PARSING PROCESS ----------------

print("\n--------------------------------------------------")
print("STACK\t\tINPUT\t\tACTION")
print("--------------------------------------------------")

while len(stack) > 0:

    top = stack[-1]

    current = input_string[pointer]

    stack_string = "".join(stack)

    remaining_input = input_string[pointer:]

    # MATCH
    if top == current:

        print(stack_string,
              "\t\t",
              remaining_input,
              "\t\tMatch", current)

        stack.pop()
        pointer += 1

        # ACCEPT
        if top == '$':
            print("\nSTRING ACCEPTED")
            break

    # NON TERMINAL
    elif is_non_terminal(top):

        key = (top, current)

        if key in table:

            production = table[key]

            print(stack_string,
                  "\t\t",
                  remaining_input,
                  "\t\t",
                  top, "->", production)

            stack.pop()

            # push reverse
            if production != 'e':

                for symbol in reversed(production):
                    stack.append(symbol)

        else:

            print(stack_string,
                  "\t\t",
                  remaining_input,
                  "\t\tERROR")

            print("\nSTRING REJECTED")
            break

    # ERROR
    else:

        print(stack_string,
              "\t\t",
              remaining_input,
              "\t\tERROR")

        print("\nSTRING REJECTED")
        break





































Let’s solve one **LL(1)** sample question by hand that matches your `4_LL1.py` predictive parser. [geeksforgeeks](https://www.geeksforgeeks.org/compiler-design/construction-of-ll1-parsing-table/)

The grammar in your file is:

- \(E \to TA\)  
- \(A \to +TA \mid e\)  
- \(T \to FB\)  
- \(B \to *FB \mid e\)  
- \(F \to (E) \mid i\) [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

This is the classic expression grammar for `i + i * i`-style inputs.

We will do a full **LL(1) parse** of a sample string by hand:

\[
\text{input } = i+i*i
\]

Remember, your code automatically appends `$` at the end, so we will parse `i+i*i$`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

***

## Step 1: Write the LL(1) parsing table (given)

Your program stores the table as: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

- `M[E, i] = TA`  
- `M[E, (] = TA`  

- `M[A, +] = +TA`  
- `M[A, )] = e`  
- `M[A, $] = e`  

- `M[T, i] = FB`  
- `M[T, (] = FB`  

- `M[B, +] = e`  
- `M[B, *] = *FB`  
- `M[B, )] = e`  
- `M[B, $] = e`  

- `M[F, i] = i`  
- `M[F, (] = (E)`  

In exam, they usually give the grammar and ask you to **construct this table**, but here we will assume table is known and focus on using it to parse. [geeksforgeeks](https://www.geeksforgeeks.org/compiler-design/construction-of-ll1-parsing-table/)

***

## Step 2: LL(1) parse of `i+i*i$` by hand

Initialization (just like your code): [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

- Stack: `[$, E]` (E is start symbol, $ is bottom-of-stack marker)  
- Input: `i + i * i $`  

We repeatedly look at:  
- top of stack (TOS)  
- current input symbol  

and follow rules:

- If TOS is terminal and equals input → **Match** (pop stack, advance input).  
- If TOS is non-terminal → use table entry `M[TOS, input]` to pick production.  
- If no entry → ERROR. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

Now trace step-by-step:

1. **Stack:** `E$` (top E), **Input:** `i+i*i$`  
   - TOS = E (non-terminal), input symbol = `i`  
   - Use table: `M[E, i] = TA`.  
   - Action: pop E, push `A` then `T` (reverse of `TA`).  
   - New stack: `AT$`.

2. **Stack:** `AT$` (top A), **Input:** `i+i*i$`  
   - TOS = A (non-terminal), input symbol = `i`.  
   - No `M[A, i]` entry; but note, in actual LL(1), A only uses FIRST and FOLLOW. Here we see A’s productions are for `+` and FOLLOW entries (`)` and `$`). Since current input is `i`, matching will happen via T, not A yet.  
   - However, in your table, A is not used with `i`, so correct step is actually: we mis-ordered push: from `TA`, T is at top in code (since you push reversed). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

   So let’s correct stack order consistent with file:

   After step 1, when E → TA, code does:

   - `stack.pop()` E  
   - push reversed("TA") = 'A', then 'T'  
   - So stack is `$`, `A`, `T`; T is on top. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

   So we should track as `T A $` with T on top.

   Rewriting step 1 result:

   1. Stack top-to-bottom: `T A $`, Input: `i+i*i$`.

3. **Step 2 (corrected)**  
   - TOS = T, current input = `i`.  
   - `M[T, i] = FB`.  
   - Pop T, push `B`, then `F`.  
   - Stack: `B F A $`.

4. **Step 3**  
   - TOS = F, input = `i`.  
   - `M[F, i] = i`.  
   - Pop F, push `i`.  
   - Stack: `B i A $`.

5. **Step 4**  
   - TOS = `i` (terminal), input = `i`.  
   - Match i: pop stack, advance input.  
   - Stack: `B A $`.  
   - Input now: `+i*i$`.

6. **Step 5**  
   - TOS = B (non-terminal), input = `+`.  
   - `M[B, +] = e`.  
   - So apply B → e; pop B, push nothing.  
   - Stack: `A $`.

7. **Step 6**  
   - TOS = A, input = `+`.  
   - `M[A, +] = +TA`.  
   - Pop A, push `A`, `T`, `+` (reverse of `+TA`).  
   - Stack: `A T + $`.

8. **Step 7**  
   - TOS = `+`, input = `+`.  
   - Match `+`: pop, advance input.  
   - Stack: `A T $`.  
   - Input: `i*i$`.

9. **Step 8**  
   - TOS = T, input = `i`.  
   - `M[T, i] = FB`.  
   - Pop T, push `B`, `F`.  
   - Stack: `A B F $`.

10. **Step 9**  
    - TOS = F, input = `i`.  
    - `M[F, i] = i`.  
    - Pop F, push `i`.  
    - Stack: `A B i $`.

11. **Step 10**  
    - TOS = `i`, input = `i`.  
    - Match `i`.  
    - Stack: `A B $`.  
    - Input: `*i$`.

12. **Step 11**  
    - TOS = B, input = `*`.  
    - `M[B, *] = *FB`.  
    - Pop B, push `B`, `F`, `*`.  
    - Stack: `A B F * $`.

13. **Step 12**  
    - TOS = `*`, input = `*`.  
    - Match `*`.  
    - Stack: `A B F $`.  
    - Input: `i$`.

14. **Step 13**  
    - TOS = F, input = `i`.  
    - `M[F, i] = i`.  
    - Pop F, push `i`.  
    - Stack: `A B i $`.

15. **Step 14**  
    - TOS = `i`, input = `i`.  
    - Match `i`.  
    - Stack: `A B $`.  
    - Input: `$`.

16. **Step 15**  
    - TOS = B, input = `$`.  
    - `M[B, $] = e`.  
    - Pop B.  
    - Stack: `A $`.

17. **Step 16**  
    - TOS = A, input = `$`.  
    - `M[A, $] = e`.  
    - Pop A.  
    - Stack: `$`.

18. **Step 17**  
    - TOS = `$`, input = `$`.  
    - Match `$`, stack becomes empty, input ends → **ACCEPT**. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

This is exactly the sequence your LL(1) parser would print in its STACK / INPUT / ACTION columns for `i+i*i`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17600239-920d-41bd-a417-93a2f58e3035/4_LL1.py)

***

When you sit in the exam, they often ask: “Construct LL(1) table and parse the string `i+i*i`.” You can now copy this stack trace pattern: at each step, show stack, input, and action (production or match).  

To cement this, what string would you like to try next by hand in this same grammar—maybe `(i+i)*i` or `i*i+i`—so you can practice running the LL(1) steps yourself?
