# MapReader/player.py

from typing import List, Optional


class Player:
    class Town:
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

        @staticmethod
        def from_int(value: int):
            for name, val in Player.Town.__dict__.items():
                if not name.startswith("__") and val == value:
                    return val
            return Player.Town.Random

    class PlayerColor:
        Red = 0
        Blue = 1
        Tan = 2
        Green = 3
        Orange = 4
        Purple = 5
        Teal = 6
        Pink = 7

    def __init__(self):
        self.player_color: Optional[int] = None  # PlayerColor
        self.allowed_towns: List[int] = []  # List of Town enums
        self.is_random_town: bool = False
        self.has_main_town: bool = False
        self.is_towns_set: bool = False
        self.generate_hero_at_main_town: bool = False
        self.generate_hero: bool = False
        self.has_random_hero: bool = False
        self.main_custom_hero_id: Optional[int] = None
        self.main_town_type: Optional[int] = None  # Town
        self.main_town_x: int = 0
        self.main_town_y: int = 0
        self.main_town_z: int = 0
