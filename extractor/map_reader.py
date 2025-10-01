# extractor/map_reader.py

import struct
import json

SIZES = {
    36: "S",
    72: "M",
    108: "L",
    144: "XL",
    180: "XXL"
}


class H3MParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}

    def get_map_size(self):
        try:
            with open(self.file_path, "rb") as f:
                f.seek(0x1A)
                size = struct.unpack("<I", f.read(4))[0]
            return SIZES.get(size, "Unknown")
        except Exception as e:
            print(f"Ошибка при чтении размера карты {self.file_path}: {e}")
            return "Unknown"

    def parse_metadata(self):
        try:
            with open(self.file_path, "rb") as f:
                f.seek(0)
                header = f.read(128)  # прочитать заголовок
                # TODO: Распарсить названия карты, автора и т.д.
                self.data["metadata"] = {
                    "name": "Unknown",
                    "author": "Unknown"
                }
        except Exception as e:
            print(f"Ошибка при чтении метаданных: {e}")

    def parse_terrain(self):
        # TODO: реализовать чтение ландшафта карты
        self.data["terrain"] = "Not implemented"

    def parse_objects(self):
        # TODO: реализовать чтение объектов на карте
        self.data["objects"] = "Not implemented"

    def parse(self):
        self.data["file"] = self.file_path
        self.data["size"] = self.get_map_size()
        self.parse_metadata()
        self.parse_terrain()
        self.parse_objects()

    def to_json(self):
        return json.dumps(self.data, indent=4)
