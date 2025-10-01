# map_object.py
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional

from .def_info import DefInfo
from .player import Player


class Town(Enum):
    CASTLE = 0
    RAMPART = 1
    TOWER = 2
    INFERNO = 3
    NECROPOLIS = 4
    DUNGEON = 5
    STRONGHOLD = 6
    FORTRESS = 7
    CONFLUX = 8


# --- Resource defs ---
RESOURCES: List[str] = [
    "avtwood0.def",
    "avtore0.def",
    "avtsulf0.def",
    "avtmerc0.def",
    "avtcrys0.def",
    "avtgems0.def",
    "avtgold0.def",
]

# --- Dwellings ---
DWELLINGS: Dict[int, List[str]] = {
    Town.CASTLE.value: [
        "AVGpike0.def",
        "AVGcros0.def",
        "AVGgrff0.def",
        "AVGswor0.def",
        "AVGmonk0.def",
        "AVGcavl0.def",
        "AVGangl0.def",
    ],
    Town.RAMPART.value: [
        "AVGcent0.def",
        "AVGdwrf0.def",
        "AVGelf0.def",
        "AVGpega0.def",
        "AVGtree0.def",
        "AVGunic0.def",
        "AVGgdrg0.def",
    ],
    Town.TOWER.value: [
        "AVGgrem0.def",
        "AVGgarg0.def",
        "AVGgolm0.def",
        "AVGmage0.def",
        "AVGgeni0.def",
        "AVGnaga0.def",
        "AVGtitn0.def",
    ],
    Town.INFERNO.value: [
        "AVGimp0.def",
        "AVGgogs0.def",
        "AVGhell0.def",
        "AVGdemn0.def",
        "AVGpit0.def",
        "AVGefre0.def",
        "AVGdevl0.def",
    ],
    Town.NECROPOLIS.value: [
        "AVGskel0.def",
        "AVGzomb0.def",
        "AVGwght0.def",
        "AVGvamp0.def",
        "AVGlich0.def",
        "AVGbkni0.def",
        "AVGbone0.def",
    ],
    Town.DUNGEON.value: [
        "AVGtrog0.def",
        "AVGharp0.def",
        "AVGbhld0.def",
        "AVGmdsa0.def",
        "AVGmino0.def",
        "AVGmant0.def",
        "AVGrdrg0.def",
    ],
    Town.STRONGHOLD.value: [
        "AVGgobl0.def",
        "AVGwolf0.def",
        "AVGorcg0.def",
        "AVGogre0.def",
        "AVGrocs0.def",
        "AVGcycl0.def",
        "AVGbhmt0.def",
    ],
    Town.FORTRESS.value: [
        "AVGgnll0.def",
        "AVGlzrd0.def",
        "AVGdfly0.def",
        "AVGbasl0.def",
        "AVGgorg0.def",
        "AVGwyvn0.def",
        "AVGhydr0.def",
    ],
    Town.CONFLUX.value: [
        "AVGpixie.def",
        "AVGair0.def",
        "AVGwatr0.def",
        "AVGfire0.def",
        "AVGerth0.def",
        "AVGelp.def",
        "AVGfbrd.def",
    ],
}

# --- Monsters (по уровням) ---
MONSTERS: Dict[int, List[str]] = {
    1: [
        "AvWPike.def", "AVWpikx0.def", "AVWcent0.def", "AVWcenx0.def",
        "AVWgrem0.def", "AVWgrex0.def", "AVWimp0.def", "AVWimpx0.def",
        "AVWskel0.def", "AVWskex0.def", "AVWtrog0.def", "AvWInfr.def",
        "AVWgobl0.def", "AVWgobx0.def", "AVWgnll0.def", "AVWgnlx0.def",
        "AVWpixie.def", "AVWsprit.def", "AVWhalf.def", "AVWpeas.def",
    ],
    2: [
        "AVWarch0.def", "AVWarhx0.def", "AVWdwrf0.def", "AVWdwrx0.def",
        "AVWgarg0.def", "AVWgarx0.def", "AVWgogs0.def", "AVWgogx0.def",
        "AVWzomb0.def", "AVWzomx0.def", "AVWharp0.def", "AVWharx0.def",
        "AVWwolf0.def", "AVWwolx0.def", "AVWlzrd0.def", "AVWlzrx0.def",
        "AVWair.def", "AVWstmr.def", "AVWboar.def", "AVWmumi.def",
    ],
    3: [
        "AVWgrff0.def", "AVWgrfx0.def", "AVWelf0.def", "AVWelfx0.def",
        "AVWgolm0.def", "AVWgolx0.def", "AVWhell0.def", "AVWhelx0.def",
        "AVWwght0.def", "AVWwgthx0.def", "AVWbhld0.def", "AVWbhlx0.def",
        "AVWorc0.def", "AVWorcx0.def", "AVWdfly.def", "AVWdrgx0.def",
        "AVWwatl.def", "AVWicee.def", "AVWrog.def", "AVWNtrogl.def",
    ],
    4: [
        "AVWswor0.def", "AVWswozx0.def", "AVWpega0.def", "AVWpegx0.def",
        "AVWmage0.def", "AVWmagx0.def", "AVWdemn0.def", "AVWdemx0.def",
        "AVWvamp0.def", "AVWvmpx0.def", "AVWmdsa0.def", "AVWmdsx0.def",
        "AVWogre0.def", "AVWogrx0.def", "AVWbasl0.def", "AVWbasx0.def",
        "AVWfire.def", "AVWele.def", "AVWnomd.def", "AVWshar.def",
    ],
    5: [
        "AVWmonk0.def", "AVWmonx0.def", "AVWtree0.def", "AVWtrex0.def",
        "AVWgeni0.def", "AVWgenx0.def", "AVWpit0.def", "AVWpitz0.def",
        "AVWlich0.def", "AVWlicx0.def", "AVWmino0.def", "AVWminx0.def",
        "AVWrocs0.def", "AVWrocx0.def", "AVWgorg0.def", "AVWgorx0.def",
        "AVWearth.def", "AVWpsye.def", "AVWtroo.def", "AVWsteel.def",
    ],
    6: [
        "AVWcavl0.def", "AVWcvax0.def", "AVWunio0.def", "AVWunx0.def",
        "AVWnaga0.def", "AVWnagx0.def", "AVWefre0.def", "AVWefrx0.def",
        "AVWbkni0.def", "AVWbknx0.def", "AVWmant0.def", "AVWmanx0.def",
        "AVWcycl0.def", "AVWcycx0.def", "AVWwyvn0.def", "AVWwyvx0.def",
        "AVWmagel.def", "AVWpsyl.def", "AVWelema.def", "AVWbclm.def",
    ],
    7: [
        "AVWangl0.def", "AVWangx0.def", "AVWgdrg0.def", "AVWgdrx0.def",
        "AVWtitn0.def", "AVWtitx0.def", "AVWdevl0.def", "AVWdevx0.def",
        "AVWbone0.def", "AVWbonx0.def", "AVWrdrg0.def", "AVWrdrx0.def",
        "AVWbhmt0.def", "AVWbhmx0.def", "AVWhydr0.def", "AVWhydx0.def",
        "AVWphoenix.def", "AVWfaer.dr.def", "AVWsg.dr.def", "AVWcrag.def",
    ],
}

from enum import Enum


class Obj(Enum):
    NO_OBJ = -1
    ALTAR_OF_SACRIFICE = 2
    ANCHOR_POINT = 3
    ARENA = 4
    ARTIFACT = 5
    PANDORAS_BOX = 6
    BLACK_MARKET = 7
    BOAT = 8
    BORDERGUARD = 9
    KEYMASTER = 10
    BUOY = 11
    CAMPFIRE = 12
    CARTOGRAPHER = 13
    SWAN_POND = 14
    COVER_OF_DARKNESS = 15
    CREATURE_GENERATOR1 = 16
    CREATURE_GENERATOR2 = 17
    CREATURE_GENERATOR3 = 18
    CREATURE_GENERATOR4 = 19
    CURSED_GROUND1 = 20
    CORPSE = 21
    MARLETTO_TOWER = 22
    DERELICT_SHIP = 23
    DRAGON_UTOPIA = 24
    EVENT = 25
    EYE_OF_MAGI = 26
    FAERIE_RING = 27
    FLOTSAM = 28
    FOUNTAIN_OF_FORTUNE = 29
    FOUNTAIN_OF_YOUTH = 30
    GARDEN_OF_REVELATION = 31
    GARRISON = 32
    HERO = 33
    HILL_FORT = 34
    GRAIL = 35
    HUT_OF_MAGI = 36
    IDOL_OF_FORTUNE = 37
    LEAN_TO = 38
    LIBRARY_OF_ENLIGHTENMENT = 39
    LIGHTHOUSE = 40
    MONOLITH1 = 41
    MONOLITH2 = 42
    MONOLITH3 = 43
    MONOLITH4 = 44
    MAGIC_PLAINS1 = 45
    SCHOOL_OF_MAGIC = 46
    MAGIC_SPRING = 47
    MAGIC_WELL = 48
    MERCENARY_CAMP = 49
    MERMAID = 50
    MINE = 51
    MONSTER = 52
    MYSTICAL_GARDEN = 53
    OASIS = 54
    OBELISK = 55
    REDWOOD_OBSERVATORY = 56
    OCEAN_BOTTLE = 57
    PILLAR_OF_FIRE = 58
    PYRAMID = 59
    RALLY_FLAG = 60
    RANDOM_ART = 61
    RANDOM_TREASURE_ART = 62
    RANDOM_MINOR_ART = 63
    RANDOM_MAJOR_ART = 64
    RANDOM_RELIC_ART = 65
    RANDOM_HERO = 66
    RANDOM_MONSTER = 67
    RANDOM_MONSTER_L1 = 68
    RANDOM_MONSTER_L2 = 69
    RANDOM_MONSTER_L3 = 70
    RANDOM_MONSTER_L4 = 71
    RANDOM_RESOURCE = 72
    RANDOM_TOWN = 73
    RANDOM_CASTLE = 74
    RANDOM_DWELLING = 75
    RESOURCE = 76
    SANCTUARY = 77
    SCHOLAR = 78
    SEA_CHEST = 79
    SEER_HUT = 80
    CRYPT = 81
    SHIPWRECK = 82
    SHIPWRECK_SURVIVOR = 83
    SHIPYARD = 84
    SHRINE_OF_MAGIC_INCANTATION = 85
    SHRINE_OF_MAGIC_GESTURE = 86
    SHRINE_OF_MAGIC_THOUGHT = 87
    SIGN = 88
    SIRENS = 89
    SPELL_SCROLL = 90
    STABLES = 91
    TAVERN = 92
    TEMPLE = 93
    DEN_OF_THIEVES = 94
    TOWN = 95
    TRADING_POST = 96
    LEARNING_STONE = 97
    TREASURE_CHEST = 98
    TREE_OF_KNOWLEDGE = 99
    SUBTERRANEAN_GATE = 100
    UNIVERSITY = 101
    WAGON = 102
    WAR_MACHINE_FACTORY = 103
    SCHOOL_OF_WAR = 104
    WARRIORS_TOMB = 105
    WATER_WHEEL = 106
    WATERING_HOLE = 107
    WHIRLPOOL = 108
    WINDMILL = 109
    WITCH_HUT = 110
    HOLE = 111
    RANDOM_MONSTER_L5 = 112
    RANDOM_MONSTER_L6 = 113
    RANDOM_MONSTER_L7 = 114
    BRUSH = 115
    BUSH = 116
    CACTUS = 117
    CANYON = 118
    CRATER = 119
    DEAD_VEGETATION = 120
    FLOWERS = 121
    FROZEN_LAKE = 122
    HEDGE = 123
    HILL = 124
    LAKE = 125
    LAVA_FLOW = 126
    LAVA_LAKE = 127
    MUSHROOMS = 128
    LOG = 129
    MANDRAKE = 130
    MOSS = 131
    MOUND = 132
    MOUNTAIN = 133
    OAK_TREES = 134
    OUTCROPPING = 135
    PINES = 136
    PLANT = 137
    RANDOM_MONSTER_L8 = 138
    RANDOM_MONSTER_L9 = 139
    RANDOM_MONSTER_L10 = 140
    RANDOM_MONSTER_L11 = 141
    RANDOM_MONSTER_L12 = 142
    RANDOM_MONSTER_L13 = 143
    RANDOM_MONSTER_L14 = 144
    RANDOM_MONSTER_L15 = 145
    RANDOM_MONSTER_L16 = 146
    RANDOM_MONSTER_L17 = 147
    RANDOM_MONSTER_L18 = 148
    RANDOM_MONSTER_L19 = 149
    RANDOM_MONSTER_L20 = 150
    DESERT_HILLS = 151
    ROCKS = 152
    SAND_DUNE = 153
    SHRUB = 154
    STALAGMITE = 155
    STUMP = 156
    TAR_PIT = 157
    TREES = 158
    VOLCANIC_MOUNTAIN = 159
    VOLCANO = 160
    WATER_LAKE = 161
    WATERFALL = 162
    REEF = 163
    RANDOM_MONSTER_L21 = 164
    RANDOM_MONSTER_L22 = 165
    RANDOM_MONSTER_L23 = 166
    RANDOM_MONSTER_L24 = 167
    RANDOM_MONSTER_L25 = 168
    RANDOM_MONSTER_L26 = 169
    RANDOM_MONSTER_L27 = 170
    RANDOM_MONSTER_L28 = 171
    RANDOM_MONSTER_L29 = 172
    RANDOM_MONSTER_L30 = 173
    RANDOM_MONSTER_L31 = 174
    RANDOM_MONSTER_L32 = 175
    RANDOM_MONSTER_L33 = 176
    RANDOM_MONSTER_L34 = 177
    RANDOM_MONSTER_L35 = 178
    RANDOM_MONSTER_L36 = 179
    RANDOM_MONSTER_L37 = 180
    RANDOM_MONSTER_L38 = 181
    RANDOM_MONSTER_L39 = 182
    RANDOM_MONSTER_L40 = 183
    MOUNTAIN2 = 184
    TREES2 = 185
    VOLCANO2 = 186
    CACTUS2 = 187
    MOUNTAIN3 = 188
    TREES3 = 189
    VOLCANO3 = 190
    CACTUS3 = 191
    MOUNTAIN4 = 192
    TREES4 = 193
    VOLCANO4 = 194
    CACTUS4 = 195
    MOUNTAIN5 = 196
    TREES5 = 197
    VOLCANO5 = 198
    CACTUS5 = 199
    MOUNTAIN6 = 200
    TREES6 = 201
    VOLCANO6 = 202
    CACTUS6 = 203
    MOUNTAIN7 = 204
    TREES7 = 205
    VOLCANO7 = 206
    CACTUS7 = 207
    MOUNTAIN8 = 208
    TREES8 = 209
    VOLCANO8 = 210
    CACTUS8 = 211
    MOUNTAIN9 = 212
    TREES9 = 213
    VOLCANO9 = 214
    CACTUS9 = 215
    MOUNTAIN10 = 216
    TREES10 = 217
    VOLCANO10 = 218
    CACTUS10 = 219
    MOUNTAIN11 = 220
    TREES11 = 221
    VOLCANO11 = 222
    CACTUS11 = 223
    MOUNTAIN12 = 224
    TREES12 = 225
    VOLCANO12 = 226
    CACTUS12 = 227
    MOUNTAIN13 = 228
    TREES13 = 229
    VOLCANO13 = 230
    ROCKLANDS = 231

    @staticmethod
    def from_int(value: int) -> "Obj":
        for obj in Obj:
            if obj.value == value:
                return obj
        return Obj.NO_OBJ


class SeerHutRewardType(Enum):
    NOTHING = 0
    EXPERIENCE = 1
    MANA_POINTS = 2
    MORALE_BONUS = 3
    LUCK_BONUS = 4
    RESOURCES = 5
    PRIMARY_SKILL = 6
    SECONDARY_SKILL = 7
    ARTIFACT = 8
    SPELL = 9
    CREATURE = 10


@dataclass
class MapObject:
    x: int
    y: int
    z: int
    def_info: Optional[DefInfo] = None
    obj: Optional[Obj] = None
    owner: Optional[Player] = None

    # --- Random helpers ---
    @staticmethod
    def get_random_monster_def_name() -> str:
        level = random.randint(1, 6)
        monsters_defs = MONSTERS[level]
        return random.choice(monsters_defs)

    @staticmethod
    def get_random_monster_def_name_by_level(level: int) -> str:
        monsters_defs = MONSTERS.get(level, [])
        return random.choice(monsters_defs) if monsters_defs else ""

    @staticmethod
    def get_random_dwelling_def_name_by_level(level: int) -> str:
        if not (0 <= level < 7):
            return ""
        defs = [dw[level] for dw in DWELLINGS.values()]
        return random.choice(defs) if defs else ""

    @staticmethod
    def get_random_dwelling_def_name_by_faction_and_level(faction: int, level: int) -> str:
        return DWELLINGS[faction][level]

    @staticmethod
    def get_random_town() -> int:
        return random.randint(0, 8)

    @staticmethod
    def get_random_resource_def_name() -> str:
        return random.choice(RESOURCES)

    @staticmethod
    def get_town_def_name(town_id: int, has_fort: bool) -> str:
        mapping = {
            Town.CASTLE.value: ("avccasx0.def", "avccast0.def"),
            Town.RAMPART.value: ("avcramx0.def", "avcramp0.def"),
            Town.TOWER.value: ("avctowx0.def", "avctowr0.def"),
            Town.INFERNO.value: ("avcinfx0.def", "avcinfc0.def"),
            Town.NECROPOLIS.value: ("avcnecx0.def", "avcnecr0.def"),
            Town.DUNGEON.value: ("avcdunx0.def", "avcdung0.def"),
            Town.STRONGHOLD.value: ("avcstrx0.def", "avcstro0.def"),
            Town.FORTRESS.value: ("avcftrx0.def", "avcftrt0.def"),
            Town.CONFLUX.value: ("avchforx.def", "avchfor0.def"),
        }
        return mapping.get(town_id, ("avcrand0.def", "avcrand0.def"))[0 if has_fort else 1]


class Art:
    ART_SPECIAL = 0
    ART_TREASURE = 1
    ART_MINOR = 2
    ART_MAJOR = 3
    ART_RELIC = 4
    ART_ANY = 5

    CLASSES = ["S", "T", "M", "J", "R"]

    def __init__(self, rarity_class: str, name: str):
        self.rarity_class = rarity_class
        self.name = name

    @staticmethod
    def get_random_art_id(art_level: int) -> int:
        if art_level == Art.ART_RELIC:
            min_id, max_id = 129, 141
        else:
            min_id, max_id = 10, 128

        art_id = random.randint(min_id, max_id)
        if art_id == 128:  # Pandora’s box — skip
            return Art.get_random_art_id(art_level)
        return art_id

    def __str__(self) -> str:
        return f"{self.rarity_class} {self.name}"
