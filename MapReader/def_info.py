# MapReader/def_info.py

from .bits import BitSet

class DefInfo:
    def __init__(self):
        self.sprite_name: str = ""
        self.passable_cells: BitSet = BitSet()
        self.active_cells: BitSet = BitSet()
        self.placement_order: int = 0
        self.object_id: int = 0
        self.object_class_sub_id: int = 0

    def clone(self) -> "DefInfo":
        """Returns a shallow copy of this DefInfo."""
        new_def_info = DefInfo()
        new_def_info.sprite_name = self.sprite_name
        new_def_info.passable_cells = BitSet.from_long(self.passable_cells.to_long())
        new_def_info.active_cells = BitSet.from_long(self.active_cells.to_long())
        new_def_info.placement_order = self.placement_order
        new_def_info.object_id = self.object_id
        new_def_info.object_class_sub_id = self.object_class_sub_id
        return new_def_info

    def __str__(self) -> str:
        return self.sprite_name.lower().replace(".def", "")

    def is_visitable(self) -> bool:
        """Returns True if there are any active cells."""
        return self.active_cells.length() > 0
