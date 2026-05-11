# Generate D Record, R Record
# and Local Symbol Table

# ---------------- INPUT ASM PROGRAM ----------------

program = [

    "PG1 START 0000",
    "EXTDEF A, B",
    "EXTREF C, D",
    "ADD ABC",
    "A SUB PQR",
    "ADD ABC1",
    "B MUL ABC",
    "END"
]


# ---------------- VARIABLES ----------------

location_counter = 0

extdef = []

extref = []

symbol_table = {}


# ---------------- PROCESS ----------------

for line in program:

    words = line.replace(",", "").split()

    # START
    if "START" in line:

        location_counter = int(words[2], 16)

    # EXTDEF
    elif words[0] == "EXTDEF":

        extdef = words[1:]

    # EXTREF
    elif words[0] == "EXTREF":

        extref = words[1:]

    # END
    elif words[0] == "END":

        break

    else:

        # label present
        if len(words) == 3:

            label = words[0]

            symbol_table[label] = \
                hex(location_counter)[2:].zfill(6).upper()

        # each instruction = 3 bytes
        location_counter += 3


# ---------------- D RECORD ----------------

d_record = "D"

for symbol in extdef:

    if symbol in symbol_table:

        d_record += "^" + symbol + "^" + symbol_table[symbol]


# ---------------- R RECORD ----------------

r_record = "R"

for symbol in extref:

    r_record += "^" + symbol


# ---------------- OUTPUT ----------------

print("\nD RECORD\n")

print(d_record)

print("\nR RECORD\n")

print(r_record)


# ---------------- LOCAL SYMBOL TABLE ----------------

print("\nLocal Symbol Table\n")

print("Symbol Name\tValue")

for symbol in symbol_table:

    print(symbol,
          "\t\t",
          symbol_table[symbol])