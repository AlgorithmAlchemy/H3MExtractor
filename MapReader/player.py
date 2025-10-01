# MapReader/player.py
from enum import IntEnum
from typing import List, Optional

class Player:
    class Town(IntEnum):
        Castle = 0
        Rampart = 1
        Tower = 2
        Inferno = 3
        Necropolis = 4
        Dungeon = 5
        Stronghold = 6
        Fortress = 7
        Conflux = 8
        Random = 255

    class PlayerColor(IntEnum):
        Red = 0
        Blue = 1
        Tan = 2
        Green = 3
        Orange = 4
        Purple = 5
        Teal = 6
        Pink = 7

    def __init__(self):
        self.player_color: Optional['Player.PlayerColor'] = None
        self.allowed_towns: List['Player.Town'] = []
        self.is_random_town: bool = False
        self.has_main_town: bool = False
        self.is_towns_set: bool = False
        self.generate_hero_at_main_town: bool = False
        self.generate_hero: bool = False
        self.has_random_hero: bool = False
        self.main_custom_hero_id: Optional[int] = None
        self.main_town_type: Optional['Player.Town'] = None
        self.main_town_x: int = 0
        self.main_town_y: int = 0
        self.main_town_z: int = 0
