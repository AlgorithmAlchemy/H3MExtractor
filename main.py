# main.py

import sys
import json
from pathlib import Path
from bitarray import bitarray
from MapReader.map_reader import MapReader


class BitSetSerializer(json.JSONEncoder):
    """Serializer for BitSet-like objects (bitarray)."""

    def default(self, obj):
        if isinstance(obj, bitarray):
            # Преобразуем в массив чисел типа long (64-бит)
            long_array = []
            bits = obj.tolist()
            for i in range(0, len(bits), 64):
                chunk = bits[i:i + 64]
                value = 0
                for bit_index, bit in enumerate(chunk):
                    if bit:
                        value |= 1 << bit_index
                long_array.append(value)
            return long_array
        return super().default(obj)


def is_homm_map_file(path: Path) -> bool:
    return path.suffix.lower() == ".h3m"


def write_to_json_safe(path: Path, output_folder: Path):
    try:
        write_to_json(path, output_folder)
    except Exception as e:
        print(f"Error processing {path}: {e}")


def write_to_json(path: Path, output_folder: Path):
    print(path.name)
    output_name = output_folder / f"{path.name}.json"
    with path.open("rb") as f:
        map_reader = MapReader(f)
        map_obj = map_reader.read()
    with output_name.open("w", encoding="utf-8") as f:
        json.dump(map_obj, f, indent=4, cls=BitSetSerializer)


def main():
    if len(sys.argv) < 3:
        print("Bad arguments")
        sys.exit(1)

    input_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])
    output_folder.mkdir(parents=True, exist_ok=True)

    for path in input_folder.rglob("*"):
        if path.is_file() and is_homm_map_file(path):
            write_to_json_safe(path, output_folder)


if __name__ == "__main__":
    if len(sys.argv) == 1:  # запуск без аргументов (например, из PyCharm)
        maps_folder = Path("Maps")
        # Найти первый .h3m файл в папке Maps
        first_map = next(maps_folder.glob("*.h3m"), None)
        if first_map is None:
            print("No .h3m files found in Maps folder for debug run")
            sys.exit(1)

        sys.argv.extend([
            str(first_map.parent),  # входная папка
            "Output"                # папка для результата
        ])
        print(f"[DEBUG] Using map {first_map.name}")

    main()
