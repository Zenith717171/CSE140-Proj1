# Opcodes (7-bit)
OP_R      = "0110011"
OP_IMM    = "0010011"
OP_LOAD   = "0000011"
OP_STORE  = "0100011"
OP_BRANCH = "1100011"
OP_JALR   = "1100111"
OP_JAL    = "1101111"

# R-type: (funct3, funct7) -> op
R_TYPE_TABLE = {
    ("000", "0000000"): "add",
    ("000", "0100000"): "sub",
    ("111", "0000000"): "and",
    ("110", "0000000"): "or",
    ("100", "0000000"): "xor",
    ("001", "0000000"): "sll",
    ("101", "0000000"): "srl",
    ("101", "0100000"): "sra",
    ("010", "0000000"): "slt",
    ("011", "0000000"): "sltu",
}

# I-type OP-IMM: funct3 plus sometimes funct7 (for shifts)
# We'll handle shifts in decoder logic; table for the rest:
I_IMM_SIMPLE = {
    "000": "addi",
    "010": "slti",
    "011": "sltiu",
    "100": "xori",
    "110": "ori",
    "111": "andi",
}

# LOAD: funct3 -> op
LOAD_TABLE = {
    "000": "lb",
    "001": "lh",
    "010": "lw",
}

# STORE: funct3 -> op
STORE_TABLE = {
    "000": "sb",
    "001": "sh",
    "010": "sw",
}

# BRANCH: funct3 -> op
BRANCH_TABLE = {
    "000": "beq",
    "001": "bne",
    "100": "blt",
    "101": "bge",
}