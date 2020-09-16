from constants import *
from util import dice
import random


class Fighter:
    def __init__(self, hp=0, mp=0, defense=0, str=0, dex=0, int=0, unarmed_attack=(1, 1, 1), attack_speed=DEFAULT_ATTACK_SPEED,
                 evasion=0, hit_rate=100, xp_reward=0, current_xp=0, level=1, ability_points=0):
        self.hp = hp
        self.base_max_hp = self.hp
        self.mp = mp
        self.base_max_mp = self.mp

        self.base_strength = str
        self.base_dexterity = dex
        self.base_intelligence = int

        self.unarmed_attack = unarmed_attack
        self.base_defense = defense
        self.base_evasion = evasion
        self.hit_rate = hit_rate
        self.attack_speed = attack_speed

        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points

        self.damage = None

    def get_dict(self):
        result = {}
        result["hp"] = self.hp
        result["max_hp"] = self.base_max_hp
        result["mp"] = self.mp
        result["max_mp"] = self.base_max_mp

        result["strength"] = self.base_strength
        result["dexterity"] = self.base_dexterity
        result["intelligence"] = self.base_intelligence

        result["unarmed_attack"] = self.unarmed_attack
        result["defense"] = self.base_defense
        result["evasion"] = self.base_evasion
        result["hit_rate"] = self.hit_rate
        result["attack_speed"] = self.attack_speed

        result["xp_reward"] = self.xp_reward
        result["current_xp"] = self.current_xp
        result["level"] = self.level
        result["ability_points"] = self.ability_points

        return result

    def restore_from_dict(self, result):
        self.hp = result["hp"]
        self.base_max_hp = result["max_hp"]
        self.mp = result["mp"]
        self.base_max_mp = result["max_mp"]

        self.base_strength = result["strength"]
        self.base_dexterity = result["dexterity"]
        self.base_intelligence = result["intelligence"]

        self.unarmed_attack = result["unarmed_attack"]
        self.base_defense = result["defense"]
        self.base_evasion = result["evasion"]
        self.hit_rate = result["hit_rate"]
        self.attack_speed = result["attack_speed"]

        self.xp_reward = result["xp_reward"]
        self.current_xp = result["current_xp"]
        self.level = result["level"]
        self.ability_points = result["ability_points"]

    @property
    def max_hp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_hp"]

        return self.base_max_hp + bonus

    @property
    def max_mp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_mp"]

        return self.base_max_mp + bonus

    @property
    def str(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["str"]

        return self.base_strength + bonus

    @property
    def dex(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["dex"]

        return self.base_dexterity + bonus

    @property
    def int(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["int"]

        return self.base_intelligence + bonus

    @property
    def defense(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["defense"]

        return self.base_defense + bonus

    @property
    def evasion(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["evasion"]

        return self.base_evasion + bonus + (self.dex / 2)

    @property
    def melee_attack_damage(self):
        if self.owner.equipment and self.owner.equipment.melee_weapon_damage:
            D, min_d, max_d = self.owner.equipment.melee_weapon_damage
        else:
            D, min_d, max_d = self.owner.fighter.unarmed_attack

        melee_attack_damage = dice(D, min_d+(self.dex//3), max_d+self.str)

        return melee_attack_damage

    @property
    def ranged_attack_damage(self):
        if self.owner.equipment and self.owner.equipment.ranged_weapon_damage:
            D, min_d, max_d = self.owner.equipment.ranged_weapon_damage

            ranged_attack_damage = dice(D, min_d+(self.str//3), max_d+self.dex)

            return ranged_attack_damage

    def hit_chance(self, target, ranged=None):
        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        hit = None

        if not ranged:
            if self.owner.equipment and self.owner.equipment.weapon_hit_rate:
                hit = self.owner.equipment.weapon_hit_rate
            else:
                hit = self.owner.fighter.hit_rate

        elif ranged:
            if self.owner.equipment and self.owner.equipment.ranged_hit_rate:
                hit = self.owner.equipment.ranged_hit_rate
        if hit:

            hit_chance = (hit / 100) * \
                (1 - (target.fighter.evasion / 100)) * 100

            return hit_chance

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            self.owner.blocks = False
            self.owner.is_dead = True
            results.append({"dead": self.owner})
            print(f"{self.owner.name} is dead x!")

        return results

    def attack(self, target, ranged=None):
        results = []

        if ranged:
            if random.randrange(1, 100) <= self.hit_chance(target, ranged=True):
                self.damage = self.ranged_attack_damage // target.fighter.defense

        elif not ranged:
            if random.randrange(1, 100) <= self.hit_chance(target):
                self.damage = self.melee_attack_damage // target.fighter.defense

        if self.damage:
            if self.damage >= 0:
                # damage表示メッセージを格納する
                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(self.damage)} hit points."})
                results.extend(target.fighter.take_damage(self.damage))

                # xp獲得処理
                if target.is_dead:
                    self.current_xp += target.fighter.xp_reward

            else:
                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no self.damage"}
                )

            results.extend([{"damage_pop": target, "damage": self.damage}])

        else:
            results.append(
                {"message": f"{self.owner.name.capitalize()} attacks {target.name} Avoided"}
            )

        return results
