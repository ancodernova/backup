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