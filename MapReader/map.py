# MapReader/map.py

from typing import List, Dict
from bitset import BitSet  # наш предыдущий класс BitSet
from player import Player  # нужно будет переписать Player.py
from tile import Tile  # нужно будет переписать Tile.py
from map_object import MapObject  # нужно будет переписать MapObject.py


class Map:
    class Version:
        Unknown = 0
        ROE = 0x0E  # 14
        AB = 0x15  # 21
        SOD = 0x1C  # 28
        WOG = 0x33  # 51

        @staticmethod
        def from_int(value: int):
            for v_name, v_value in Map.Version.__dict__.items():
                if not v_name.startswith("__") and v_value == value:
                    return v_value
            return Map.Version.Unknown

    def __init__(self):
        self.version: int = Map.Version.Unknown
        self.size: int = 0
        self.has_underground: bool = False
        self.title: str = ""
        self.description: str = ""
        self.players: List[Player] = []
        self.available_artifacts: BitSet = BitSet()
        self.tiles: List[Tile] = []
        self.objects: List[MapObject] = []
        self.towns: Dict[int, int] = {}
