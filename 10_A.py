# SIC Program Blocks

program = [

    "START 1000",

    "USE CODE",
    "LDA ALPHA",
    "STA BETA",

    "USE DATA",
    "RESW 2",

    "USE EXTRA",
    "LDA GAMMA",

    "END"
]


# ---------------- VARIABLES ----------------

blocks = {}

current_block = "DEFAULT"

start_address = 0x1000


# ---------------- PROCESS ----------------

for line in program:

    words = line.split()

    # START
    if words[0] == "START":

        start_address = int(words[1], 16)

    # USE
    elif words[0] == "USE":

        current_block = words[1]

        if current_block not in blocks:
            blocks[current_block] = 0

    # END
    elif words[0] == "END":
        break

    else:

        if current_block not in blocks:
            blocks[current_block] = 0

        # RESW
        if words[0] == "RESW":

            blocks[current_block] += int(words[1]) * 3

        else:
            blocks[current_block] += 3


# ---------------- OUTPUT ----------------

print("\nPROGRAM BLOCK TABLE\n")

print("Block\tStart Address\tLength")

address = start_address

for block in blocks:

    print(block,
          "\t",
          hex(address)[2:].upper(),
          "\t\t",
          blocks[block])

    address += blocks[block]