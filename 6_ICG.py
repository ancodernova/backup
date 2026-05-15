# Intermediate Code Generation
# Infix to Postfix + Quadruple + Triple

stack = []

operators = ['+', '-', '*', '/', '=']

precedence = {
    '=': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


# ---------------- INFIX TO POSTFIX ----------------

def infix_to_postfix(expression):

    output = []

    op_stack = []

    for ch in expression:

        # operand
        if ch.isalnum():

            output.append(ch)

        # opening bracket
        elif ch == '(':

            op_stack.append(ch)

        # closing bracket
        elif ch == ')':

            while op_stack and op_stack[-1] != '(':
                output.append(op_stack.pop())

            op_stack.pop()

        # operator
        else:

            while (op_stack and op_stack[-1] != '(' and
                   precedence[op_stack[-1]] >= precedence[ch]):

                output.append(op_stack.pop())

            op_stack.append(ch)

    # remaining operators
    while op_stack:
        output.append(op_stack.pop())

    return output


# ---------------- INPUT ----------------

choice = input("Enter expression type (infix/postfix): ")

# INFIX
if choice == "infix":

    expr = input("Enter infix expression: ")

    postfix = infix_to_postfix(expr)

# POSTFIX
else:

    postfix = input("Enter postfix expression: ").split()


# if infix conversion used
if isinstance(postfix, list) == False:
    postfix = list(postfix)

print("\nPostfix Expression:")
print(" ".join(postfix))


# ---------------- ICG ----------------

temp_count = 1

quadruple = []
triple = []

for symbol in postfix:

    # operand
    if symbol not in operators:

        stack.append(symbol)

    # operator
    else:

        operand2 = stack.pop()
        operand1 = stack.pop()

        temp = "T" + str(temp_count)

        # ---------- QUADRUPLE ----------
        quadruple.append([symbol, operand1, operand2, temp])

        # ---------- TRIPLE ----------
        op1 = operand1
        op2 = operand2

        if operand1.startswith("T"):
            op1 = "(" + str(int(operand1[1:]) - 1) + ")"

        if operand2.startswith("T"):
            op2 = "(" + str(int(operand2[1:]) - 1) + ")"

        triple.append([symbol, op1, op2])

        stack.append(temp)

        temp_count += 1


# ---------------- QUADRUPLE ----------------

print("\nQuadruple Representation:\n")

print("Operator\tArg1\tArg2\tResult")

for row in quadruple:

    print(row[0],
          "\t\t",
          row[1],
          "\t",
          row[2],
          "\t",
          row[3])


# ---------------- TRIPLE ----------------

print("\nTriple Representation:\n")

print("Index\tOperator\tArg1\tArg2")

for i in range(len(triple)):

    row = triple[i]

    print(i,
          "\t",
          row[0],
          "\t\t",
          row[1],
          "\t",
          row[2])









































Let’s move to the next file in your pipeline: `6_ICG.py` – **Intermediate Code Generation (ICG)** for arithmetic expressions. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

This script does exactly what exam questions on “generate three-address code / quadruples / triples for an expression” ask you to do by hand. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

***

## What this program does

- Optionally converts an **infix expression** (like `a=b+c*d`) to **postfix**. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)
- Scans the postfix expression and generates:
  - **Quadruples**: \((op, arg1, arg2, result)\).  
  - **Triples**: \((index, op, arg1, arg2)\), where arg1/arg2 may refer to previous results by index. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

Operators it supports: `+ - * / =` with precedence `* / > + - > =`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

***

## How to run this file (with example)

1. Save as `6_ICG.py`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)
2. Run:  
   ```bash
   python 6_ICG.py
   ```  
3. When asked:  
   - `Enter expression type (infix/postfix):` → type `infix`.  
   - `Enter infix expression:` → try something like `a=b+c*d`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

The program will:
- Convert to postfix.  
- Generate quadruple and triple tables and print them. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

Try that once and keep the output in front of you; then the exam method below will make more sense.

***

## Code logic (short walkthrough)

### 1. Infix → postfix

`infix_to_postfix(expression)` uses the usual stack-based algorithm: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

- For operands (letters/digits): append to output.  
- For `(`: push to op_stack.  
- For `)`: pop operators until `(`.  
- For operators: while top of op_stack has greater/equal precedence, pop it to output; then push current operator.  
- At end: pop remaining operators to output. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

This yields a list of postfix symbols like `['a', 'b', 'c', 'd', '*', '+', '=']` for `a=b+c*d`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

### 2. Core ICG loop

- Maintain `stack` of operands / temporaries. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)
- For each symbol in postfix:
  - If operand: push to stack.  
  - If operator:  
    - Pop `operand2`, then `operand1`.  
    - Create a new temporary `Ti`.  
    - Append a quadruple `[op, operand1, operand2, Ti]`.  
    - For triple:
      - Use actual operand names, or `(index)` if operand itself is a temp.  
      - Append `[op, op1, op2]`.  
    - Push `Ti` back on stack.  
    - Increment temp_count. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

At the end, quadruple and triple tables are printed. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

***

## Sample exam-style question and solution

**Question:**  
Generate three-address code, quadruple and triple representations for:

\[
E: a = b + c * d
\]

### Step 1: Convert infix to postfix

Expression: `a = b + c * d`  

Operator precedence: `*` > `+` > `=`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

Postfix:  
\[
a\ b\ c\ d\ *\ +\ =
\]

That’s exactly what your program’s `infix_to_postfix` would produce. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

### Step 2: Process postfix to generate temporaries

Use a stack:

1. Read `a` → operand → push: stack = [a]  
2. `b` → stack = [a, b]  
3. `c` → stack = [a, b, c]  
4. `d` → stack = [a, b, c, d]  
5. `*` → operator:  
   - Pop operand2 = `d`, operand1 = `c`.  
   - New temp `T1 = c * d`.  
   - Push `T1`.  
   - Stack = [a, b, T1]  
   - Quadruple: (`*`, `c`, `d`, `T1`)  
   - Triple: `(0, *, c, d)`  (index 0).  

6. `+` → operator:  
   - Pop operand2 = `T1`, operand1 = `b`.  
   - New temp `T2 = b + T1`.  
   - Stack = [a, T2]  
   - Quadruple: (`+`, `b`, `T1`, `T2`)  
   - Triple:
     - operand1 `b`, operand2 `T1` refers to previous temp at index 0 → `(0)`.  
     - So triple: `(1, +, b, (0))`.  

7. `=` → operator:  
   - Pop operand2 = `T2`, operand1 = `a`.  
   - `a = T2`.  
   - Stack = [T3] (if you also create a temp; often we treat result as `a` directly in exams, but your code uses `T3`).  
   - Quadruple: (`=`, `a`, `T2`, `T3`) or conceptually `=, T2, -, a` depending on convention. In your program: operator `=`, arg1 `a`, arg2 `T2`, result `T3`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)
   - Triple: `(2, =, a, (1))`.  

So the **three-address form** (ignoring final temp naming) is:

- `T1 = c * d`  
- `T2 = b + T1`  
- `a = T2`  

Which is exactly what they usually want in an intermediate code generation question, and matches the structure of your quadruples/triples. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

In your program’s specific quadruple layout, rows would look like: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

| Operator | Arg1 | Arg2 | Result |
|----------|------|------|--------|
| *        | c    | d    | T1     |
| +        | b    | T1   | T2     |
| =        | a    | T2   | T3     |

And triples:

| Index | Op | Arg1 | Arg2 |
|-------|----|------|------|
| 0     | *  | c    | d    |
| 1     | +  | b    | (0)  |
| 2     | =  | a    | (1)  |

Your code differs slightly (it always uses new T’s and references prior temps by `(index)` in triple), but the exam marker mainly cares about correct sequence and use of temporaries. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/128210935/1f98cfe9-b93b-498b-b02d-a259a63b6276/6_ICG.py)

***

Now, to make this stick: if the exam question gives `x = (a + b) * (c - d)`, can you outline what the postfix would be and how many temporaries you’d need before expanding into full quadruple/triple form?
