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