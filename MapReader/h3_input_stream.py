# MapReader/h3_input_stream.py

import io
import struct

class H3InputStream:
    def __init__(self, stream: io.BufferedReader):
        self.stream = stream
        self.buffer: bytes = b""
        self.pos: int = 0
        self.mark_pos: int = 0

    def to_int(self, b: bytes, byte_count: int) -> int:
        if byte_count == 1:
            return b[0]
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
        return self.read_bytes(1)[0]

    def read_bool(self) -> bool:
        return self.read_byte() == 1

    def read_string_length(self) -> int:
        data = self.read_bytes(4)
        return struct.unpack("<i", data)[0]

    def read_string(self) -> str:
        length = self.read_string_length()
        if length > 64000:
            raise IOError(f"Read String is too long: {length}")
        data = self.read_bytes(length)
        return data.decode("utf-8")

    def read_bytes(self, length: int) -> bytes:
        data = self.stream.read(length)
        if not data or len(data) != length:
            raise IOError(f"Could not read {length} bytes from stream")
        self.pos += length
        self.buffer = data
        return data

    def get_position(self) -> int:
        return self.pos

    def skip(self, skip: int) -> int:
        current_pos = self.stream.tell()
        self.stream.seek(skip, io.SEEK_CUR)
        skipped = self.stream.tell() - current_pos
        self.pos += skipped
        return skipped

    def mark(self):
        """Marks the current position."""
        self.mark_pos = self.stream.tell()

    def reset(self):
        """Resets to the last marked position."""
        if not hasattr(self.stream, "seek"):
            raise IOError("Mark/reset not supported")
        self.stream.seek(self.mark_pos)
        self.pos = self.mark_pos
