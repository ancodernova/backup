# SIC Assembler
# H Record, E Record and Symbol Table

# INPUT PROGRAM

program = [

    "PG2 START 1000",
    "JMP ADD1",
    "JMP ADD2",
    "ADD1 LDA #1020",
    "STA #3040",
    "ADD2 LDA #1004",
    "DATA1 BYTE C='ABC'",
    "DATA2 EQU 10",
    "END"
]


# ---------------- OPCODES ----------------

opcode = ["LDA", "STA", "JMP"]


# ---------------- VARIABLES ----------------

symbol_table = {}

start_address = 0

location_counter = 0

program_name = ""


# ---------------- PASS 1 ----------------

for line in program:

    words = line.split()

    # START
    if "START" in line:

        program_name = words[0]

        start_address = int(words[2], 16)

        location_counter = start_address

        continue

    # END
    if words[0] == "END":
        break

    label = ""

    # LABEL PRESENT
    if words[0] not in opcode and words[0] not in ["BYTE", "EQU"]:

        label = words[0]

        words = words[1:]

    mnemonic = words[0]

    operand = words[1] if len(words) > 1 else ""

    # STORE SYMBOL
    if label:

        if mnemonic == "EQU":

            symbol_table[label] = operand

        else:

            symbol_table[label] = hex(location_counter)[2:].upper()

    # LOCATION COUNTER UPDATE

    if mnemonic in opcode:

        location_counter += 3

    elif mnemonic == "BYTE":

        value = operand.split("'")[1]

        location_counter += len(value)


# ---------------- PROGRAM LENGTH ----------------

program_length = location_counter - start_address


# ---------------- H RECORD ----------------

header = "H^" + \
         program_name + "^" + \
         hex(start_address)[2:].zfill(6).upper() + "^" + \
         hex(program_length)[2:].zfill(6).upper()


# ---------------- E RECORD ----------------

end_record = "E^" + \
             hex(start_address)[2:].zfill(6).upper()


# ---------------- OUTPUT ----------------

print("\nH RECORD\n")

print(header)

print("\nE RECORD\n")

print(end_record)


# ---------------- SYMBOL TABLE ----------------

print("\nSYMBOL TABLE\n")

print("Symbol Name\tValue")

for symbol in symbol_table:

    print(symbol,
          "\t\t",
          symbol_table[symbol])