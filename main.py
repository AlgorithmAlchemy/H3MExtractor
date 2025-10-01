import struct
import json

SIZES = {
    36: "S",
    72: "M",
    108: "L",
    144: "XL",
    180: "XXL"
}


def get_map_size(file_path: str) -> str:
    """Читает размер карты из .h3m файла."""
    try:
        with open(file_path, "rb") as f:
            f.seek(0x1A)  # смещение, где хранится размер
            size = struct.unpack("<I", f.read(4))[0]
        return SIZES.get(size, "Unknown")
    except Exception as e:
        print(f"Ошибка при чтении карты {file_path}: {e}")
        return None


def map_to_json(file_path: str):
    """Преобразует .h3m карту в JSON формат."""
    size = get_map_size(file_path)
    if size:
        map_data = {
            "file": file_path,
            "size": size
        }
        json_data = json.dumps(map_data, indent=4)
        print(json_data)
    else:
        print(f"Не удалось определить размер карты {file_path}.")
