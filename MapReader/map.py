# MapReader/map.py

from typing import List, Dict
from MapReader.bits import BitSet
from MapReader.player import Player
from MapReader.tile import Tile
from MapReader.map_object import MapObject


class Version:
    UNKNOWN = 0
    ROE = 0x0E
    AB = 0x15
    SOD = 0x1C
    WOG = 0x33

    @staticmethod
    def from_int(value: int):
        for name, val in Version.__dict__.items():
            if not name.startswith("__") and val == value:
                return val
        return Version.UNKNOWN


class Map:
    def __init__(self):
        self.version: int = Version.UNKNOWN
        self.size: int = 0
        self.has_underground: bool = False
        self.title: str = ""
        self.description: str = ""
        self.players: List[Player] = []
        self.available_artifacts: BitSet = BitSet()
        self.tiles: List[Tile] = []
        self.objects: List[MapObject] = []
        self.towns: Dict[int, int] = {}
