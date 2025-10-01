# MapReader/bits.py

from bitarray import bitarray


def convert_from_long(value: int) -> bitarray:
    """Converts a long integer to a bitarray (BitSet equivalent)."""
    bits = bitarray()
    bits.frombytes(value.to_bytes((value.bit_length() + 7) // 8, byteorder='little', signed=False))

    bits = bits[:value.bit_length()]
    return bits


def convert_to_long(bits: bitarray) -> int:
    """Converts a bitarray (BitSet equivalent) back to long integer."""
    value = 0
    for i, bit in enumerate(bits):
        if bit:
            value |= 1 << i
    return value
