# map_reader.py
import io
import gzip
import math
from typing import List, Optional

from .h3_input_stream import H3InputStream
from .map import Map, Version
from .player import Player
from .tile import Tile
from .def_info import DefInfo
from .bits import Bits


class MapReader:
    def __init__(self, file_stream: io.BufferedReader):
        # Java: new GZIPInputStream(fileStream)
        with gzip.GzipFile(fileobj=file_stream) as gz:
            data = gz.read()
        self.stream = H3InputStream(io.BytesIO(data))
        self.map = Map()

    # ---------- HEADER ----------
    def read_header(self):
        # map version
        self.map.version = Version.from_int(self.stream.read_int(4))
        if self.map.version == Version.UNKNOWN:
            raise IOError("Wrong map format")

        # areAnyPlayers (skip)
        self.stream.read_byte()
        self.map.size = self.stream.read_int(4)
        self.map.has_underground = self.stream.read_bool()
        self.map.title = self.stream.read_string()
        self.map.description = self.stream.read_string()

        # difficulty
        self.stream.read_byte()

        # level limit
        if self.map.version != Version.ROE:
            self.stream.read_byte()

        self.read_player_info()
        self.read_victory_loss_conditions()
        self.read_team_info()
        self.read_allowed_heroes()

    # ---------- VICTORY / LOSS ----------
    def read_victory_loss_conditions(self):
        victory_condition = self.stream.read_int(1)
        if victory_condition != 0xFF:
            # allow normal victory (applies to AI)
            self.stream.read_bytes(2)

        if victory_condition == 0x00:  # ARTIFACT
            self.stream.read_byte()
            if self.map.version != Version.ROE:
                self.stream.read_byte()
        elif victory_condition == 0x01:  # GATHERTROOP
            self.stream.read_byte()
            if self.map.version != Version.ROE:
                self.stream.read_byte()
            self.stream.read_int(4)
        elif victory_condition == 0x02:  # GATHERRESOURCE
            self.stream.read_byte()
            self.stream.read_int(4)
        elif victory_condition == 0x03:  # BUILDCITY
            self.stream.read_bytes(3)
            self.stream.read_byte()
            self.stream.read_byte()
        elif victory_condition == 0x04:  # BUILDGRAIL
            self.stream.read_bytes(3)
        elif victory_condition == 0x05:  # BEATHERO
            self.stream.read_bytes(3)
        elif victory_condition == 0x06:  # CAPTURECITY
            self.stream.read_bytes(3)
        elif victory_condition == 0x07:  # BEATMONSTER
            self.stream.read_bytes(3)
        elif victory_condition == 0x0A:  # TRANSPORTITEM
            self.stream.read_byte()
            self.stream.read_bytes(3)

        loss_condition = self.stream.read_int(1)
        if loss_condition == 0x01:  # LOSSCASTLE
            self.stream.read_bytes(3)
        elif loss_condition == 0x02:  # LOSSHERO
            self.stream.read_bytes(3)
        elif loss_condition == 0x03:  # TIMEEXPIRES
            self.stream.read_bytes(2)

    # ---------- PLAYER INFO ----------
    def read_player_info(self):
        for i in range(8):
            player = Player()
            player.player_color = Player.PlayerColor(i)

            can_human = self.stream.read_bool()
            can_ai = self.stream.read_bool()

            if not can_human and not can_ai:
                if self.map.version in (Version.SOD, Version.WOG):
                    self.stream.read_bytes(13)
                elif self.map.version == Version.AB:
                    self.stream.read_bytes(12)
                elif self.map.version == Version.ROE:
                    self.stream.read_bytes(6)
                continue

            # behavior
            self.stream.read_byte()

            # allowed towns flag
            if self.map.version in (Version.SOD, Version.WOG):
                player.is_towns_set = self.stream.read_bool()
            else:
                player.is_towns_set = True

            # allowed towns bitset
            towns_bits = Bits.convert(self.stream.read_int(1 if self.map.version == Version.ROE else 2))
            for j in range(9):
                if j in towns_bits:
                    player.allowed_towns.append(Player.Town(j))

            player.is_random_town = self.stream.read_bool()
            player.has_main_town = self.stream.read_bool()
            if player.has_main_town:
                if self.map.version != Version.ROE:
                    player.generate_hero_at_main_town = self.stream.read_bool()
                    player.generate_hero = self.stream.read_bool()
                else:
                    player.generate_hero_at_main_town = True
                    player.generate_hero = False

                player.main_town_x = self.stream.read_byte()
                player.main_town_y = self.stream.read_byte()
                player.main_town_z = self.stream.read_byte()

            # has random hero
            self.stream.read_bool()

            # custom hero
            hero_id = self.stream.read_int(1)
            if hero_id != 0xFF:
                self.stream.read_int(1)  # portrait
                self.stream.read_string()  # hero name

            if self.map.version != Version.ROE:
                self.stream.read_byte()  # unknown
                hero_count = self.stream.read_int(4)
                for _ in range(hero_count):
                    self.stream.skip(1)  # hero id
                    self.stream.read_string()

            self.map.players.append(player)

    # ---------- TEAMS ----------
    def read_team_info(self):
        teams_count = self.stream.read_int(1)
        if teams_count > 0:
            for _ in range(8):
                self.stream.read_byte()

    # ---------- HEROES ----------
    def read_allowed_heroes(self):
        bytes_count = 16 if self.map.version == Version.ROE else 20
        self.stream.read_bytes(bytes_count)
        if self.map.version != Version.ROE:
            placeholders_qty = self.stream.read_int(4)
            self.stream.read_bytes(placeholders_qty)

    def read_disposed_heroes(self):
        if self.map.version in (Version.SOD, Version.WOG):
            heroes_count = self.stream.read_int(1)
            for _ in range(heroes_count):
                self.stream.read_byte()  # id
                self.stream.read_byte()  # portrait
                self.stream.read_string()  # name
                self.stream.read_byte()  # players
        self.stream.read_bytes(31)

    def read_allowed_artifacts(self):
        if self.map.version != Version.ROE:
            bytes_count = 17 if self.map.version == Version.AB else 18
            self.stream.read_bytes(bytes_count)

    def read_allowed_spells_abilities(self):
        if self.map.version in (Version.SOD, Version.WOG):
            self.stream.read_bytes(9)  # spells
            self.stream.read_bytes(4)  # abilities

    def read_rumors(self):
        rumors_count = self.stream.read_int(4)
        for _ in range(rumors_count):
            self.stream.read_string()  # name
            self.stream.read_string()  # text

    # ---------- HERO DATA ----------
    def load_artifact_to_slot(self):
        if self.map.version == Version.ROE:
            self.stream.read_int(1)
        else:
            self.stream.read_int(2)

    def read_predefined_heroes(self):
        if self.map.version in (Version.SOD, Version.WOG):
            for _ in range(156):
                if not self.stream.read_bool():
                    continue
                if self.stream.read_bool():
                    self.stream.read_int(4)  # exp
                if self.stream.read_bool():
                    skills_count = self.stream.read_int(4)
                    for _ in range(skills_count):
                        self.stream.read_byte()
                        self.stream.read_byte()
                self.load_artifacts_of_hero()
                if self.stream.read_bool():
                    self.stream.read_string()  # bio
                self.stream.read_byte()  # sex
                if self.stream.read_bool():
                    self.stream.read_bytes(9)  # spells
                if self.stream.read_bool():
                    self.stream.read_bytes(4)  # primary skills

    # ---------- TILES / TERRAIN ----------
    def read_terrain(self):
        size = int(math.pow(self.map.size, 2)) * (2 if self.map.has_underground else 1)
        for _ in range(size):
            tile = Tile()
            tile.terrain = Tile.TerrainType(self.stream.read_int(1))
            tile.terrain_image_index = self.stream.read_int(1)
            tile.river = Tile.RiverType(self.stream.read_int(1))
            tile.river_image_index = self.stream.read_int(1)
            tile.road = Tile.RoadType(self.stream.read_int(1))
            tile.road_image_index = self.stream.read_int(1)

            mirror_conf = self.stream.read_byte()
            tile.flip_conf = Bits.convert(mirror_conf)
            self.map.tiles.append(tile)

    # ---------- DEF INFO ----------
    def read_def_info(self) -> List[DefInfo]:
        defs: List[DefInfo] = []
        defs_count = self.stream.read_int(4)
        for _ in range(defs_count):
            d = DefInfo()
            d.sprite_name = self.stream.read_string()
            d.passable_cells = Bits.convert((self.stream.read_int(4) << 32) | (self.stream.read_int(2) & 0xFFFFFFF))
            d.active_cells = Bits.convert((self.stream.read_int(4) << 32) | (self.stream.read_int(2) & 0xFFFFFFF))
            self.stream.skip(2)  # terrain type
            self.stream.skip(2)  # terrain group
            d.object_id = self.stream.read_int(4)
            d.object_class_sub_id = self.stream.read_int(4)
            self.stream.skip(1)  # objects group
            d.placement_order = self.stream.read_int(1)
            self.stream.skip(16)  # nulls
            defs.append(d)
        return defs

    # ---------- MISC ----------
    def read_creature_set(self, creatures_count: int):
        for _ in range(creatures_count):
            self.stream.skip(2 if self.map.version != Version.ROE else 1)
            self.stream.skip(2)

    def read_message_and_guards(self):
        if self.stream.read_bool():
            self.stream.read_string()
            if self.stream.read_bool():
                self.read_creature_set(7)
            self.stream.skip(4)

    def read_resources(self):
        for _ in range(7):
            self.stream.skip(4)

    def load_artifacts_of_hero(self):
        if self.stream.read_bool():
            for _ in range(16):
                self.load_artifact_to_slot()
            if self.map.version in (Version.SOD, Version.WOG):
                self.load_artifact_to_slot()
            self.load_artifact_to_slot()  # spellbook
            if self.map.version != Version.ROE:
                self.load_artifact_to_slot()
            else:
                self.stream.read_byte()
            arts_count = self.stream.read_int(2)
            for _ in range(arts_count):
                self.load_artifact_to_slot()

    def read_hero(self):
        if self.map.version != Version.ROE:
            self.stream.skip(4)  # id
        self.stream.skip(1)  # owner
        self.stream.skip(1)  # sub id

        if self.stream.read_bool():  # has name
            self.stream.read_string()

        if self.map.version not in (Version.ROE, Version.AB):
            if self.stream.read_bool():  # has exp
                self.stream.read_int(4)
        else:
            self.stream.read_int(4)

        if self.stream.read_bool():  # portrait
            self.stream.read_int(1)

        if self.stream.read_bool():  # secondary skills
            skills_count = self.stream.read_int(4)
            self.stream.skip(skills_count * 2)

        if self.stream.read_bool():  # garrison
            self.read_creature_set(7)

        self.stream.read_int(1)  # formation
        self.load_artifacts_of_hero()
        self.stream.read_int(1)  # patrol radius

        if self.map.version != Version.ROE:
            if self.stream.read_bool():  # custom bio
                self.stream.read_string()
            self.stream.read_int(1)  # sex

        if self.map.version not in (Version.ROE, Version.AB):
            if self.stream.read_bool():  # custom spells
                self.stream.skip(9)
        elif self.map.version == Version.AB:
            self.stream.skip(1)

        if self.map.version not in (Version.ROE, Version.AB):
            if self.stream.read_bool():  # primary skills
                self.stream.skip(4)

        self.stream.skip(16)

    def read_quest(self, mission_type: int):
        if mission_type == 0:
            return
        elif mission_type in (2, 1, 3, 4):
            self.stream.skip(4)
        elif mission_type == 5:
            art_num = self.stream.read_int(1)
            self.stream.skip(art_num * 2)
        elif mission_type == 6:
            type_num = self.stream.read_int(1)
            self.stream.read_int(type_num * 2 * 2)
        elif mission_type == 7:
            self.stream.skip(7 * 4)
        elif mission_type in (8, 9):
            self.stream.skip(1)

        self.stream.skip(4)
        self.stream.read_string()  # first visit
        self.stream.read_string()  # next visit
        self.stream.read_string()  # completed

    def read_town(self) -> int:
        town_identifier = 0
        if self.map.version != Version.ROE:
            town_identifier = self.stream.read_int(4)

        self.stream.read_int(1)  # owner

        if self.stream.read_bool():  # name
            self.stream.read_string()

        if self.stream.read_bool():  # garrison
            self.read_creature_set(7)

        self.stream.read_int(1)  # formation

        if self.stream.read_bool():  # custom buildings
            self.stream.skip(6)
            self.stream.skip(6)
        else:
            self.stream.read_bool()  # has fort

        if self.map.version != Version.ROE:
            self.stream.skip(9)

        self.stream.skip(9)

        castle_events = self.stream.read_int(4)
        for _ in range(castle_events):
            self.stream.read_string()
            self.stream.read_string()
            self.read_resources()
            self.stream.read_int(1)  # players_affected

            if self.map.version != Version.ROE:
                self.stream.read_int(1)  # human_affected

            self.stream.skip(1)  # ai
            self.stream.skip(2)  # day
            self.stream.skip(2)  # iteration
            self.stream.skip(16)
            self.stream.skip(6)
            self.stream.skip(7 * 2)
            self.stream.skip(4)

        if self.map.version not in (Version.ROE, Version.AB):
            self.stream.skip(1)  # alignment

        self.stream.skip(3)
        return town_identifier

    def read_objects(self, defs: List[DefInfo]):
        objects_count = self.stream.read_int(4)
        for _ in range(objects_count):
            obj = MapObject()
            obj.x = self.stream.read_int(1)
            obj.y = self.stream.read_int(1)
            obj.z = self.stream.read_int(1)
            idx = self.stream.read_int(4)

            if idx >= len(defs) or idx < 0:
                raise IOError(f"Parse error: bad def index {idx}")

            obj.def_info = defs[idx].clone()
            obj.obj = MapObject.Obj.from_int(obj.def_info.objectId)

            self.stream.skip(5)

            # --- тут надо перенести большой switch-case по object.obj ---
            # (мы можем разобрать его по шагам отдельно, он длинный)

            if obj.obj != MapObject.Obj.GRAIL:
                self.map.objects.append(obj)

        self.map.objects.sort(reverse=True)
        print(f"Map contains {len(self.map.objects)} objects")

    def read(self) -> Map:
        self.read_header()
        self.read_disposed_heroes()
        self.read_allowed_artifacts()
        self.read_allowed_spells_abilities()
        self.read_rumors()
        self.read_predefined_heroes()
        self.read_terrain()
        defs = self.read_def_info()
        self.read_objects(defs)
        return self.map
