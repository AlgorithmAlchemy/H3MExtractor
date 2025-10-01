# MapReader/bits.py
from typing import Set

from bitarray import bitarray


class BitSet:
    """Simple BitSet wrapper using bitarray (like Java's BitSet)."""

    def __init__(self, size: int = 0):
        self.bits = bitarray(size)
        self.bits.setall(0)

    def set(self, index: int, value: bool = True):
        """Set bit at position index."""
        if index >= len(self.bits):
            self.bits.extend([0] * (index + 1 - len(self.bits)))
        self.bits[index] = value

    def get(self, index: int) -> bool:
        """Get bit at position index."""
        if index < len(self.bits):
            return self.bits[index]
        return False

    def clear(self, index: int = None):
        """Clear one bit or all bits if index is None."""
        if index is None:
            self.bits.setall(0)
        else:
            if index < len(self.bits):
                self.bits[index] = 0

    def is_empty(self) -> bool:
        """Check if no bits are set."""
        return not self.bits.any()

    def to_long(self) -> int:
        """Convert bitset to int."""
        value = 0
        for i, bit in enumerate(self.bits):
            if bit:
                value |= 1 << i
        return value

    @staticmethod
    def from_long(value: int) -> "BitSet":
        """Convert int to BitSet."""
        bits = BitSet()
        i = 0
        while value:
            if value & 1:
                bits.set(i, True)
            value >>= 1
            i += 1
        return bits

    @staticmethod
    def convert(value: int) -> Set[int]:
        """Convert int to a set of bit indices."""
        bits = set()
        i = 0
        while value:
            if value & 1:
                bits.add(i)
            value >>= 1
            i += 1
        return bits

    def __len__(self):
        return len(self.bits)

    def __repr__(self):
        return f"BitSet({self.to_long()})"
