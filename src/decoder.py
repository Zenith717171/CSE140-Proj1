from dataclasses import dataclass
from typing import Optional, Dict, Any

from .bit_utils import slice_bits, bits_as_int, sign_extend, hex_masked
from .isa_tables import (
    OP_R, OP_IMM, OP_LOAD, OP_STORE, OP_BRANCH, OP_JALR, OP_JAL,
    R_TYPE_TABLE, I_IMM_SIMPLE, LOAD_TABLE, STORE_TABLE, BRANCH_TABLE
)


@dataclass
class Decoded:
    inst_type: str
    operation: str
    fields: Dict[str, Any]


def decode(instr: str) -> Decoded:
    instr = instr.strip()
    opcode = slice_bits(instr, 6, 0)

    if opcode == OP_R:
        return decode_r(instr)
    if opcode in (OP_IMM, OP_LOAD, OP_JALR):
        return decode_i(instr, opcode)
    if opcode == OP_STORE:
        return decode_s(instr)
    if opcode == OP_BRANCH:
        return decode_sb(instr)
    if opcode == OP_JAL:
        return decode_uj(instr)

    # Lab says inputs will be valid, so this should not happen.
    raise ValueError(f"Unsupported opcode: {opcode}")


def reg_name(reg_bits: str) -> str:
    return f"x{bits_as_int(reg_bits)}"


def decode_r(instr: str) -> Decoded:
    rd = slice_bits(instr, 11, 7)
    funct3 = slice_bits(instr, 14, 12)
    rs1 = slice_bits(instr, 19, 15)
    rs2 = slice_bits(instr, 24, 20)
    funct7 = slice_bits(instr, 31, 25)

    op = R_TYPE_TABLE[(funct3, funct7)]

    fields = {
        "Rs1": reg_name(rs1),
        "Rs2": reg_name(rs2),
        "Rd": reg_name(rd),
        "Funct3": bits_as_int(funct3),
        "Funct7": bits_as_int(funct7),
    }
    return Decoded("R", op, fields)


def decode_i(instr: str, opcode: str) -> Decoded:
    rd = slice_bits(instr, 11, 7)
    funct3 = slice_bits(instr, 14, 12)
    rs1 = slice_bits(instr, 19, 15)
    imm12_bits = slice_bits(instr, 31, 20)
    imm_u = bits_as_int(imm12_bits)
    imm_s = sign_extend(imm_u, 12)

    # Determine operation based on opcode group
    if opcode == OP_LOAD:
        op = LOAD_TABLE[funct3]
        imm_val = imm_s
    elif opcode == OP_JALR:
        # Only jalr in your test list. funct3 should be 000.
        op = "jalr"
        imm_val = imm_s
    else:
        # OP-IMM includes shifts that need funct7 check (slli/srli/srai)
        if funct3 == "001":
            # slli: funct7 must be 0000000, shamt is imm[4:0]
            op = "slli"
            shamt = bits_as_int(slice_bits(instr, 24, 20))
            imm_val = shamt
        elif funct3 == "101":
            # srli vs srai depends on funct7
            funct7 = slice_bits(instr, 31, 25)
            shamt = bits_as_int(slice_bits(instr, 24, 20))
            op = "srai" if funct7 == "0100000" else "srli"
            imm_val = shamt
        else:
            op = I_IMM_SIMPLE[funct3]
            imm_val = imm_s

    fields = {
        "Rs1": reg_name(rs1),
        "Rd": reg_name(rd),
        "Immediate": imm_val,
        "_imm_hex": hex_masked(imm_u, 12),
    }
    return Decoded("I", op, fields)


def decode_s(instr: str) -> Decoded:
    imm_hi = slice_bits(instr, 31, 25)   # imm[11:5]
    rs2 = slice_bits(instr, 24, 20)
    rs1 = slice_bits(instr, 19, 15)
    funct3 = slice_bits(instr, 14, 12)
    imm_lo = slice_bits(instr, 11, 7)    # imm[4:0]

    imm_bits = imm_hi + imm_lo
    imm_u = bits_as_int(imm_bits)
    imm_s = sign_extend(imm_u, 12)

    op = STORE_TABLE[funct3]
    fields = {
        "Rs1": reg_name(rs1),
        "Rs2": reg_name(rs2),
        "Immediate": imm_s,
        "_imm_hex": hex_masked(imm_u, 12),
    }
    return Decoded("S", op, fields)


def decode_sb(instr: str) -> Decoded:
    rs2 = slice_bits(instr, 24, 20)
    rs1 = slice_bits(instr, 19, 15)
    funct3 = slice_bits(instr, 14, 12)

    # SB immediate bits assembly:
    # imm[12] = bit31
    # imm[10:5] = bits30:25
    # imm[4:1] = bits11:8
    # imm[11] = bit7
    b31 = slice_bits(instr, 31, 31)      # 1 bit
    b30_25 = slice_bits(instr, 30, 25)   # 6 bits
    b11_8 = slice_bits(instr, 11, 8)     # 4 bits
    b7 = slice_bits(instr, 7, 7)         # 1 bit

    imm_bits = b31 + b7 + b30_25 + b11_8 + "0"  # 13 bits including bit0=0
    imm_u = bits_as_int(imm_bits)
    imm_s = sign_extend(imm_u, 13)

    op = BRANCH_TABLE[funct3]
    fields = {
        "Rs1": reg_name(rs1),
        "Rs2": reg_name(rs2),
        "Immediate": imm_s,
    }
    return Decoded("SB", op, fields)


def decode_uj(instr: str) -> Decoded:
    rd = slice_bits(instr, 11, 7)

    # UJ immediate bits assembly:
    # imm[20] = bit31
    # imm[10:1] = bits30:21
    # imm[11] = bit20
    # imm[19:12] = bits19:12
    b31 = slice_bits(instr, 31, 31)
    b30_21 = slice_bits(instr, 30, 21)
    b20 = slice_bits(instr, 20, 20)
    b19_12 = slice_bits(instr, 19, 12)

    imm_bits = b31 + b19_12 + b20 + b30_21 + "0"  # 21 bits including bit0=0
    imm_u = bits_as_int(imm_bits)
    imm_s = sign_extend(imm_u, 21)

    fields = {
        "Rd": reg_name(rd),
        "Immediate": imm_s,
        "_imm_hex": hex_masked(imm_u, 21),
    }
    return Decoded("UJ", "jal", fields)