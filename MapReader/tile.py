# MapReader/tile.py

from typing import Optional
from bitarray import bitarray


class Tile:
    terrain_tiles = [
        "dirttl",
        "sandtl",
        "grastl",
        "snowtl",
        "swmptl",
        "rougtl",
        "subbtl",
        "lavatl",
        "watrtl",
        "rocktl",
    ]

    river_tiles = [
        "clrrvr",
        "icyrvr",
        "mudrvr",
        "lavrvr",
    ]

    road_tiles = [
        "dirtrd",
        "gravrd",
        "cobbrd",
    ]

    class TerrainType:
        Dirt = 0
        Sand = 1
        Grass = 2
        Snow = 3
        Swamp = 4
        Rough = 5
        Subterranean = 6
        Lava = 7
        Water = 8
        Rock = 9

        @staticmethod
        def to_string(value: int) -> str:
            return Tile.terrain_tiles[value]

    class RiverType:
        No = 0
        Clear = 1
        Icy = 2
        Muddy = 3
        Lava = 4

        @staticmethod
        def to_string(value: int) -> str:
            if value == Tile.RiverType.No:
                return "NONE"
            return Tile.river_tiles[value - 1]

    class RoadType:
        No = 0
        Dirt = 1
        Gravel = 2
        Cobblestone = 3

        @staticmethod
        def to_string(value: int) -> str:
            if value == Tile.RoadType.No:
                return "NONE"
            return Tile.road_tiles[value - 1]

    class TilePart:
        Terrain = "Terrain"
        Road = "Road"
        River = "River"

    def __init__(self):
        self.terrain: Optional[int] = None  # TerrainType
        self.terrain_image_index: int = 0
        self.river: Optional[int] = None  # RiverType
        self.river_image_index: int = 0
        self.road: Optional[int] = None  # RoadType
        self.road_image_index: int = 0
        self.flip_conf: bitarray = bitarray(8)  # аналог BitSet

    def to_filename(self, tile_part: str) -> str:
        if tile_part == Tile.TilePart.Terrain and self.terrain is not None:
            return Tile.TerrainType.to_string(self.terrain)
        elif tile_part == Tile.TilePart.River and self.river is not None:
            return Tile.RiverType.to_string(self.river)
        elif tile_part == Tile.TilePart.Road and self.road is not None:
            return Tile.RoadType.to_string(self.road)
        else:
            return "NONE"
