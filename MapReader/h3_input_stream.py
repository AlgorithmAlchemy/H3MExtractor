# MapReader/h3_input_stream.py

import io
import struct
from typing import BinaryIO


class H3InputStream(io.BufferedReader):
    def __init__(self, raw: BinaryIO):
        super().__init__(raw)
        self.buffer: bytes = b""
        self.pos: int = 0
        self.mark_pos: int = 0

    @staticmethod
    def to_int(b: bytes, byte_count: int) -> int:
        if byte_count == 1:
            return struct.unpack("<B", b)[0]  # unsigned byte
        elif byte_count == 2:
            return struct.unpack("<h", b)[0]
        elif byte_count == 4:
            return struct.unpack("<i", b)[0]
        else:
            raise ValueError(f"Unsupported byte count: {byte_count}")

    def read_int(self, byte_count: int) -> int:
        data = self.read_bytes(byte_count)
        return self.to_int(data, byte_count)

    def read_byte(self) -> int:
        return self.to_int(self.read_bytes(1), 1)

    def read_bool(self) -> bool:
        return self.read_byte() == 1

    def _read_string_length(self) -> int:
        data = self.read_bytes(4)
        return struct.unpack("<i", data)[0]

    def read_string(self) -> str:
        length = self._read_string_length()
        if length > 64000:
            raise IOError(f"Read String is too long: {length}")
        if length == 0:
            return ""

        data = self.read_bytes(length)
        # пробуем cp1251, если не получилось — latin1
        try:
            return data.decode("cp1251")
        except UnicodeDecodeError:
            return data.decode("latin-1", errors="replace")

    def read_bytes(self, length: int) -> bytes:
        data = super().read(length)
        if not data or len(data) != length:
            raise IOError(f"Could not read {length} bytes from stream")
        self.pos += length
        self.buffer = data
        return data

    def get_position(self) -> int:
        return self.pos

    def read(self, size: int = -1):
        data = super().read(size)
        if not data:
            return -1 if size == 1 else b""
        self.pos += len(data)
        if size == 1:
            return data[0]
        return data

    def skip(self, n: int) -> int:
        current_pos = self.tell()
        self.seek(n, io.SEEK_CUR)
        skipped = self.tell() - current_pos
        if skipped > 0:
            self.pos += skipped
        return skipped

    def mark(self, readlimit: int = 0):  # noqa: ARG002 (unused argument)
        self.mark_pos = self.pos

    def reset(self):
        self.seek(self.mark_pos)
        self.pos = self.mark_pos
