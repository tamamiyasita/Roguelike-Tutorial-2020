from dataclasses import asdict, dataclass

@dataclass
class Equippable:
    """itemの追加bonusを設定する"""
    slot:str = ""
    strength_bonus:int = 0
    defense_bonus:int = 0
    max_hp_bonus:int = 0

    def get_dict(self):
        result = {}
        result["slot"] = self.slot
        result["strength_bonus"] = self.strength_bonus
        result["defense_bonus"] = self.defense_bonus
        result["max_hp_bonus"] = self.max_hp_bonus
        return result
        # result =  asdict(Equippable())
        # return result

    def restore_from_dict(self, result):
        self.slot = result["slot"]
        self.strength_bonus = result["strength_bonus"]
        self.defense_bonus = result["defense_bonus"]
        self.max_hp_bonus = result["max_hp_bonus"]
        
