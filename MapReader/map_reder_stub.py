# map_reader_stub.py
import io
import gzip

from MapReader.h3_input_stream import H3InputStream
from MapReader.map import Map, Version


class MapReaderStub:
    def __init__(self, file_stream: io.BufferedReader):
        try:
            with gzip.GzipFile(fileobj=file_stream) as gz:
                data = gz.read()
        except (OSError, EOFError):
            file_stream.seek(0)
            data = file_stream.read()

        self.stream = H3InputStream(io.BytesIO(data))
        self.map = Map()

    def read_header(self):
        # version
        self.map.version = Version.from_int(self.stream.read_int(4))
        if self.map.version == Version.UNKNOWN:
            raise IOError("Wrong map format")

        # пропускаем байт areAnyPlayers
        self.stream.read_byte()

        # --- читаем только размер карты ---
        self.map.size = self.stream.read_int(4)
        # остальные данные не читаем
        self.map.has_underground = False
        self.map.title = ""
        self.map.description = ""

    def read(self) -> Map:
        self.read_header()
        return self.map


# ----------------- Отладка -----------------
if __name__ == "__main__":
    import os

    map_file = os.path.join("..\Maps", "One Bad Day - Allied.h3m")
    try:
        with open(map_file, "rb") as f:
            reader = MapReaderStub(f)
            map_info = reader.read()
            print(f"Map size: {map_info.size}, version: {map_info.version}")
    except Exception as e:
        print(f"Error reading map: {e}")
