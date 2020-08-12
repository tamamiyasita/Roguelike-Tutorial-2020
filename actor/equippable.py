from dataclasses import asdict, dataclass

@dataclass
class Equippable:
    """itemの追加bonusを設定する"""
    slot:str = ""
    power_bonus:int = 0
    defense_bonus:int = 0
    max_hp_bonus:int = 0

    def get_dict(self):
        # result = {}
        # result["slot"] = self.slot
        # result["power_bonus"] = self.power_bonus
        # result["defense_bonus"] = self.defense_bonus
        # result["max_hp_bonus"] = self.max_hp_bonus
        # return result
        result =  asdict(Equippable())
        return result

    def restore_from_dict(self, result):
        self.slot = result["slot"]
        self.power_bonus = result["power_bonus"]
        self.defense_bonus = result["defense_bonus"]
        self.max_hp_bonus = result["max_hp_bonus"]
        
