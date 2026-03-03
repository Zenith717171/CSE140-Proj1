# main.py
# RISC-V Instruction Decoder (CSE 140 Lab 3)
# Work Division for Demo:
#   Joe:
#     - Designed overall decoder architecture
#     - Implemented decode() dispatcher in decoder.py
#     - Implemented decode_sb() and decode_uj() including immediate bit reconstruction
#       and sign-extension logic
#
#   Noah:
#     - Implemented bit extraction utilities in bit_utils.py
#     - Implemented opcode and funct mapping tables in isa_tables.py
#     - Implemented CLI prompt and formatted output (this file)

from .decoder import decode


def print_decoded(d):
    print(f"Instruction Type: {d.inst_type}")
    print(f"Operation: {d.operation}")

    # Print fields in the order matching the lab examples
    if d.inst_type == "R":
        print(f"Rs1: {d.fields['Rs1']}")
        print(f"Rs2: {d.fields['Rs2']}")
        print(f"Rd: {d.fields['Rd']}")
        print(f"Funct3: {d.fields['Funct3']}")
        print(f"Funct7: {d.fields['Funct7']}")
    elif d.inst_type == "I":
        print(f"Rs1: {d.fields['Rs1']}")
        print(f"Rd: {d.fields['Rd']}")
        imm = d.fields["Immediate"]
        imm_hex = d.fields["_imm_hex"]
        print(f"Immediate: {imm} (or {imm_hex})")
    elif d.inst_type == "S":
        print(f"Rs1: {d.fields['Rs1']}")
        print(f"Rs2: {d.fields['Rs2']}")
        imm = d.fields["Immediate"]
        imm_hex = d.fields["_imm_hex"]
        print(f"Immediate: {imm} (or {imm_hex})")
    elif d.inst_type == "SB":
        print(f"Rs1: {d.fields['Rs1']}")
        print(f"Rs2: {d.fields['Rs2']}")
        print(f"Immediate: {d.fields['Immediate']}")
    elif d.inst_type == "UJ":
        print(f"Rd: {d.fields['Rd']}")
        imm = d.fields["Immediate"]
        imm_hex = d.fields["_imm_hex"]
        print(f"Immediate: {imm} (or {imm_hex})")


def main():
    while True:
        print("Enter an instruction:")
        s = input().strip()
        if not s:
            # continue
            break
        d = decode(s)
        print_decoded(d)
        print()  # blank line between runs, optional


if __name__ == "__main__":
    main()