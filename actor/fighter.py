from constants import *


class Fighter:
    def __init__(self, hp=0, defense=0, power=0, xp_reward=0, current_xp=0, level=1, ability_points=0):
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_max_hp = hp
        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points

    def get_dict(self):
        result = {}
        result["max_hp"] = self.base_max_hp
        result["defense"] = self.base_defense
        result["power"] = self.base_power
        result["hp"] = self.hp
        result["xp_reward"] = self.xp_reward
        result["current_xp"] = self.current_xp
        result["level"] = self.level
        result["ability_points"] = self.ability_points
        return result

    def restore_from_dict(self, result):
        self.base_max_hp = result["max_hp"]
        self.base_defense = result["defense"]
        self.base_power = result["power"]
        self.hp = result["hp"]
        self.xp_reward = result["xp_reward"]
        self.current_xp = result["current_xp"]
        self.level = result["level"]
        self.ability_points = result["ability_points"]


    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0
        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            self.owner.blocks = False
            self.owner.is_dead = True
            results.append({"dead": self.owner})
            print(f"{self.owner.name} is dead x!")

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            # damage表示メッセージを格納する
            results.append({"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points."})
            results.extend(target.fighter.take_damage(damage))

            # xp獲得処理
            if target.is_dead:
                self.current_xp += target.fighter.xp_reward

        else:
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no damage"})

        return results
