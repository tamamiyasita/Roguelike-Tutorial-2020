from constants import *
from util import dice


class Fighter:
    def __init__(self, hp=0, defense=0, strength=0, dexterity=0, unarmed_attack=(1, 1, 1), attack_speed=DEFAULT_ATTACK_SPEED,
                 hit_rate=0, xp_reward=0, current_xp=0, level=1, ability_points=0):
        self.hp = hp
        self.base_defense = defense
        self.base_strength = strength
        self.base_dexterity = dexterity
        self.base_max_hp = self.hp

            
        self.attack_speed = attack_speed
        self.hit_rate = hit_rate
        self.unarmed_attack = unarmed_attack
        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points

    def get_dict(self):
        result = {}
        result["max_hp"] = self.base_max_hp
        result["defense"] = self.base_defense
        result["strength"] = self.base_strength
        result["hp"] = self.hp
        result["xp_reward"] = self.xp_reward
        result["current_xp"] = self.current_xp
        result["level"] = self.level
        result["ability_points"] = self.ability_points
        return result

    def restore_from_dict(self, result):
        self.base_max_hp = result["max_hp"]
        self.base_defense = result["defense"]
        self.base_strength = result["strength"]
        self.hp = result["hp"]
        self.xp_reward = result["xp_reward"]
        self.current_xp = result["current_xp"]
        self.level = result["level"]
        self.ability_points = result["ability_points"]

    @property
    def attack_damage(self):
        if self.owner.equipment and self.owner.equipment.main_weapon:
            D, min_d, max_d = self.owner.equipment.main_weapon
        else:
            D, min_d, max_d = self.owner.fighter.unarmed_attack

        attack_damage = dice(D, min_d, max_d+self.strength)

        return attack_damage

    @property
    def max_hp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_hp"] + (self.strength // 3)

        return self.base_max_hp + bonus

    @property
    def strength(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["strength"]

        return self.base_strength + bonus

    @property
    def dexterity(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["dexterity"]

        return self.base_strength + bonus

    @property
    def defense(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["defense"]

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

        damage = self.attack_damage // target.fighter.defense

        if damage > 0:
            # damage表示メッセージを格納する
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points."})
            results.extend(target.fighter.take_damage(damage))

            # xp獲得処理
            if target.is_dead:
                self.current_xp += target.fighter.xp_reward

        else:
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no damage"})

        return results
