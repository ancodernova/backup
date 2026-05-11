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