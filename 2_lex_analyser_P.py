# Lexical Analyzer using State Transition Method

keywords = ["if", "else", "while", "for", "int", "switch"]

operators = ['+', '-', '*', '/', '=', '>', '<']


# ---------------- INPUT PROGRAM ----------------

code = '''
int count = 10
if count > 5
count = count + 1
'''

# add space at end for processing
code += " "


# ---------------- VARIABLES ----------------

state = 0

token = ""

print("TOKEN\t\tTYPE\n")


# ---------------- STATE TRANSITION ----------------

for ch in code:

    # ---------------- STATE 0 ----------------
    # Start State

    if state == 0:

        # Identifier or keyword starts
        if ch.isalpha() or ch == "_":

            token += ch

            state = 1

        # Number starts
        elif ch.isdigit():

            token += ch

            state = 2

        # Operator
        elif ch in operators:

            print(ch, "\t\tOPERATOR")

        # Ignore spaces
        elif ch in [' ', '\n', '\t']:

            continue

        else:

            print(ch, "\t\tINVALID")


    # ---------------- STATE 1 ----------------
    # Identifier / Keyword State

    elif state == 1:

        if ch.isalnum() or ch == "_":

            token += ch

        else:

            # keyword check
            if token in keywords:

                print(token, "\t\tKEYWORD")

            else:

                print(token, "\t\tIDENTIFIER")

            token = ""

            state = 0

            # reprocess current char
            if ch not in [' ', '\n', '\t']:

                if ch in operators:

                    print(ch, "\t\tOPERATOR")


    # ---------------- STATE 2 ----------------
    # Number State

    elif state == 2:

        if ch.isdigit():

            token += ch

        else:

            print(token, "\t\tINTEGER")

            token = ""

            state = 0

            # reprocess current char
            if ch not in [' ', '\n', '\t']:

                if ch in operators:

                    print(ch, "\t\tOPERATOR")