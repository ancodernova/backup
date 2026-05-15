# LR(1) Shift Reduce Parser

# Grammar:
# 0. E' -> E
# 1. E  -> E+T
# 2. E  -> T
# 3. T  -> T*F
# 4. T  -> F
# 5. F  -> (E)
# 6. F  -> i


# ---------------- ACTION TABLE ----------------

action = {

    (0, 'i'): 'S5',
    (0, '('): 'S4',

    (1, '+'): 'S6',
    (1, '$'): 'ACC',

    (2, '+'): 'R2',
    (2, '*'): 'S7',
    (2, ')'): 'R2',
    (2, '$'): 'R2',

    (3, '+'): 'R4',
    (3, '*'): 'R4',
    (3, ')'): 'R4',
    (3, '$'): 'R4',

    (4, 'i'): 'S5',
    (4, '('): 'S4',

    (5, '+'): 'R6',
    (5, '*'): 'R6',
    (5, ')'): 'R6',
    (5, '$'): 'R6',

    (6, 'i'): 'S5',
    (6, '('): 'S4',

    (7, 'i'): 'S5',
    (7, '('): 'S4',

    (8, '+'): 'S6',
    (8, ')'): 'S11',

    (9, '+'): 'R1',
    (9, '*'): 'S7',
    (9, ')'): 'R1',
    (9, '$'): 'R1',

    (10, '+'): 'R3',
    (10, '*'): 'R3',
    (10, ')'): 'R3',
    (10, '$'): 'R3',

    (11, '+'): 'R5',
    (11, '*'): 'R5',
    (11, ')'): 'R5',
    (11, '$'): 'R5'
}


# ---------------- GOTO TABLE ----------------

goto = {

    (0, 'E'): 1,
    (0, 'T'): 2,
    (0, 'F'): 3,

    (4, 'E'): 8,
    (4, 'T'): 2,
    (4, 'F'): 3,

    (6, 'T'): 9,
    (6, 'F'): 3,

    (7, 'F'): 10
}


# ---------------- PRODUCTIONS ----------------

productions = {

    1: ('E', 'E+T'),
    2: ('E', 'T'),
    3: ('T', 'T*F'),
    4: ('T', 'F'),
    5: ('F', '(E)'),
    6: ('F', 'i')
}


# ---------------- INPUT ----------------

input_string = input("Enter input string: ")

if input_string[-1] != '$':
    input_string += '$'


# ---------------- STACK ----------------

stack = [0]

pointer = 0


# ---------------- PRINT HEADER ----------------

print("\n----------------------------------------------------------")
print("STACK\t\tINPUT\t\tACTION")
print("----------------------------------------------------------")


# ---------------- PARSING ----------------

while True:

    state = stack[-1]

    current = input_string[pointer]

    stack_str = " ".join(map(str, stack))

    remaining = input_string[pointer:]

    # CHECK ACTION
    if (state, current) not in action:

        print(stack_str,
              "\t",
              remaining,
              "\tERROR")

        print("\nSTRING REJECTED")
        break

    act = action[(state, current)]

    # SHIFT
    if act[0] == 'S':

        next_state = int(act[1:])

        print(stack_str,
              "\t",
              remaining,
              "\tSHIFT", next_state)

        stack.append(current)
        stack.append(next_state)

        pointer += 1

    # REDUCE
    elif act[0] == 'R':

        prod_num = int(act[1:])

        left, right = productions[prod_num]

        print(stack_str,
              "\t",
              remaining,
              "\tREDUCE",
              left, "->", right)

        pop_length = len(right) * 2

        for i in range(pop_length):
            stack.pop()

        top_state = stack[-1]

        stack.append(left)

        stack.append(goto[(top_state, left)])

    # ACCEPT
    elif act == 'ACC':

        print(stack_str,
              "\t",
              remaining,
              "\tACCEPT")

        print("\nSTRING ACCEPTED")
        break














































Let’s solve one **LR(1) / canonical LR shift–reduce** sample question, matching exactly what your `4_LR1.py` does. [en.wikipedia](https://en.wikipedia.org/wiki/LR_parser)

The grammar in your file (numbered) is: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

0. \( E' \to E \)  
1. \( E \to E + T \)  
2. \( E \to T \)  
3. \( T \to T * F \)  
4. \( T \to F \)  
5. \( F \to (E) \)  
6. \( F \to i \)  

And you already have the ACTION and GOTO tables hardcoded. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

We’ll parse the same kind of string as with LL(1):

\[
\text{input } = i+i*i
\]

Your code appends `$`, so we parse `i+i*i$`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

***

## LR stack format (as in your code)

Your parser stack stores **[state, symbol, state, symbol, …, state]**. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

- Initially: `[0]` (only state 0).  
- On SHIFT:
  - push terminal, then new state.  
- On REDUCE with production \( A \to \alpha \) of length \(|\alpha|\):
  - Pop `2 * len(α)` entries (symbol+state pairs).  
  - Look at new top state, say `s`.  
  - Push `A`, then `goto[s, A]`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

We always look at `(state, current input symbol)` in ACTION table. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

***

## Step-by-step LR(1) parsing of `i+i*i$`

I’ll list stack (states and symbols), remaining input, and action.

### Step 0

- Stack: `0`  
- Input: `i+i*i$`  
- Top state = 0, current symbol = `i`.  
- ACTION(0, `i`) = `S5`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Action: **SHIFT 5**  
- Push `i`, 5.  

Stack: `0 i 5`  
Input: `+i*i$`  

***

### Step 1

- Top state = 5, current symbol = `+`.  
- ACTION(5, `+`) = `R6` (reduce by production 6: `F -> i`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Production 6: \( F \to i \), right side length = 1, so pop 2 items.

- Stack before: `0 i 5`  
- Pop `5`, `i` → stack becomes `0`.  
- Top state now = 0.  
- Push `F`, then GOTO(0, F) = 3. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 F 3`  
Input: `+i*i$`  

***

### Step 2

- Top state = 3, current symbol = `+`.  
- ACTION(3, `+`) = `R4` (production 4: `T -> F`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Production 4: \( T \to F \), |rhs| = 1 → pop 2 items.

- Stack before: `0 F 3`  
- Pop `3`, `F` → stack: `0`.  
- Top state = 0.  
- Push `T`, GOTO(0, T) = 2. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 T 2`  
Input: `+i*i$`  

***

### Step 3

- Top state = 2, current symbol = `+`.  
- ACTION(2, `+`) = `R2` (production 2: `E -> T`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Production 2: \( E \to T \), |rhs| = 1 → pop 2.

- Stack before: `0 T 2`  
- Pop `2`, `T` → stack: `0`.  
- Top state = 0.  
- Push `E`, GOTO(0, E) = 1. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1`  
Input: `+i*i$`  

***

### Step 4

- Top state = 1, current symbol = `+`.  
- ACTION(1, `+`) = `S6`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Action: **SHIFT 6**  
- Push `+`, 6.  

Stack: `0 E 1 + 6`  
Input: `i*i$`  

***

### Step 5

- Top state = 6, current symbol = `i`.  
- ACTION(6, `i`) = `S5`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

SHIFT 5:

Stack: `0 E 1 + 6 i 5`  
Input: `*i$`  

***

### Step 6

- Top state = 5, current symbol = `*`.  
- ACTION(5, `*`) = `R6` (F -> i). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Reduce by \( F \to i \):

- Pop `5`, `i` → stack: `0 E 1 + 6`.  
- Top state now = 6.  
- Push `F`, GOTO(6, F) = 3. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1 + 6 F 3`  
Input: `*i$`  

***

### Step 7

- Top state = 3, current symbol = `*`.  
- ACTION(3, `*`) = `R4` (T -> F). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Reduce by \( T \to F \):

- Pop `3`, `F` → stack: `0 E 1 + 6`.  
- Top state = 6.  
- Push `T`, GOTO(6, T) = 9. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1 + 6 T 9`  
Input: `*i$`  

***

### Step 8

- Top state = 9, current symbol = `*`.  
- ACTION(9, `*`) = `S7`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

SHIFT 7:

Stack: `0 E 1 + 6 T 9 * 7`  
Input: `i$`  

***

### Step 9

- Top state = 7, current symbol = `i`.  
- ACTION(7, `i`) = `S5`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

SHIFT 5:

Stack: `0 E 1 + 6 T 9 * 7 i 5`  
Input: `$`  

***

### Step 10

- Top state = 5, current symbol = `$`.  
- ACTION(5, `$`) = `R6` (F -> i). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Reduce by \( F \to i \):

- Pop `5`, `i` → stack: `0 E 1 + 6 T 9 * 7`.  
- Top state = 7.  
- Push `F`, GOTO(7, F) = 10. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1 + 6 T 9 * 7 F 10`  
Input: `$`  

***

### Step 11

- Top state = 10, current symbol = `$`.  
- ACTION(10, `$`) = `R3` (T -> T*F). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Production 3: \( T \to T*F \), rhs length = 3 → pop 6 items.

- Stack before: `0 E 1 + 6 T 9 * 7 F 10`  
Pop in pairs: `10 F`, `7 *`, `9 T` → stack becomes: `0 E 1 + 6`.  
- Top state = 6.  
- Push `T`, GOTO(6, T) = 9. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1 + 6 T 9`  
Input: `$`  

***

### Step 12

- Top state = 9, current symbol = `$`.  
- ACTION(9, `$`) = `R1` (E -> E+T). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Production 1: \( E \to E+T \), rhs length = 3 → pop 6 items.

- Stack before: `0 E 1 + 6 T 9`  
- Pop `9 T`, `6 +`, `1 E` → stack: `0`.  
- Top state = 0.  
- Push `E`, GOTO(0, E) = 1. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

Stack: `0 E 1`  
Input: `$`  

***

### Step 13

- Top state = 1, current symbol = `$`.  
- ACTION(1, `$`) = `ACC` (accept). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/17534756-7865-4f78-95ee-0e257a30dd6c/4_LR1.py)

So the string `i+i*i` is **accepted** by this LR(1) parser.  

This step-by-step run is exactly what your program prints in its STACK / INPUT / ACTION columns when you give input `i+i*i`. [en.wikipedia](https://en.wikipedia.org/wiki/LR_parser)

***

When you’re in the exam, the pattern is:

- Keep a table of ACTION and GOTO.  
- Maintain the stack with alternating states and symbols.  
- At each step: check `(top_state, lookahead)` in ACTION, perform Shift/Reduce/Accept, and show the stack and remaining input.  

To practice, try now to sketch the LR steps for a simpler string like `i*i` with the same grammar—how do you think the shift/reduce sequence would differ from `i+i*i`?
