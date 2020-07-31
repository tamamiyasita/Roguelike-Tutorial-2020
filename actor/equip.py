from enum import Enum

from pyglet import resource
class EquipmentSlots(Enum):
    MAIN_HAND = 1
    OFF_HAND = 2



class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        """itemの追加bonusを設定する"""
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

    def get_dict(self):
        result = {}
        result["slot"] = self.slot.name
        result["power_bonus"] = self.power_bonus
        result["defense_bonus"] = self.defense_bonus
        result["max_hp_bonus"] = self.max_hp_bonus
        return result

    def restore_from_dict(self, result):
        self.slot = EquipmentSlots[result["slot"]]
        self.power_bonus = ["power_bonus"]
        self.defense_bonus = ["defense_bonus"]
        self.max_hp_bonus = ["max_hp_bonus"]
        
