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
    import sys
    from pathlib import Path

    # Если запуск без аргументов, ищем все .h3m в папке Maps
    if len(sys.argv) == 1:
        maps_folder = Path("../Maps")
    else:
        maps_folder = Path(sys.argv[1])

    if not maps_folder.exists() or not maps_folder.is_dir():
        print(f"Folder {maps_folder} does not exist")
        sys.exit(1)

    h3m_files = list(maps_folder.glob("*.h3m"))
    if not h3m_files:
        print(f"No .h3m files found in {maps_folder}")
        sys.exit(1)

    for map_file in h3m_files:
        try:
            with open(map_file, "rb") as f:
                reader = MapReaderStub(f)
                map_info = reader.read()
                print(f"{map_file.name}: size={map_info.size}, version={map_info.version}")
        except Exception as e:
            print(f"{map_file.name}: Error reading map: {e}")