def bits_as_int(b: str) -> int:
    """Convert a binary string to int (unsigned)."""
    return int(b, 2)


def slice_bits(instr: str, hi: int, lo: int) -> str:
    """
    Return bits [hi:lo] inclusive as a string, where bit 31 is instr[0] and bit 0 is instr[31].
    Example: slice_bits(instr, 6, 0) returns the last 7 characters (opcode).
    """
    if len(instr) != 32:
        raise ValueError("Instruction must be 32 bits")
    start = 31 - hi
    end = 31 - lo
    return instr[start:end + 1]


def sign_extend(value: int, bit_width: int) -> int:
    """
    Sign-extend value interpreted as bit_width-bit signed integer to Python int.
    """
    sign_bit = 1 << (bit_width - 1)
    mask = (1 << bit_width) - 1
    value &= mask
    return (value ^ sign_bit) - sign_bit


def hex_masked(value: int, bit_width: int) -> str:
    """Return hex string like 0xFF0 masked to bit_width bits (uppercase A-F)."""
    mask = (1 << bit_width) - 1
    v = value & mask
    return "0x" + format(v, "X")