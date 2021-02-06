from actor.states.poison_status import PoisonStatus
import random
from constants import *
from util import dice, stop_watch
from actor.actor_set import *
from collections import Counter
import math


class Fighter:
    def __init__(self, hp=0, mp=0, defense=0, STR=0, DEX=0, INT=0,unarmed=None, attack_speed=DEFAULT_ATTACK_SPEED,
                 evasion=0, xp_reward=0, current_xp=0, level=1,
                 resist={"physical": 1, "fire": 1, "ice": 1, "acid": 1, "poison": 1, "mind": 1}, ability_points=0):
        self.hp = hp
        self.base_max_hp = self.hp
        self.mp = mp
        self.base_max_mp = self.mp

        self.base_strength = STR
        self.base_dexterity = DEX
        self.base_intelligence = INT

        self.unarmed = unarmed#{"damage":1, "level":1, "attr":"physical"}

        self.base_defense = defense
        self.base_evasion = evasion
        self.attack_speed = attack_speed
        self.data = {"weapon":None }
        self.resist = resist

        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points
        self._states = []

        self.level_skills = {}#level_upなどに伴う追加Skillの合計に使う
        self.base_skill_dict = skill_dict
        self._skill_list = arcade.SpriteList()
        self.equip_position = {0:(9,2), 1:(-9,3), 2:(9,-4), 3:(-11, -4), 4:(-14, 1)}



    def get_dict(self):
        result = {}

        result["hp"] = self.hp
        result["max_hp"] = self.base_max_hp

        result["strength"] = self.base_strength
        result["dexterity"] = self.base_dexterity
        result["intelligence"] = self.base_intelligence
        result["unarmed"] = self.unarmed

        result["defense"] = self.base_defense
        result["evasion"] = self.base_evasion
        result["attack_speed"] = self.attack_speed

        result["xp_reward"] = self.xp_reward
        result["current_xp"] = self.current_xp
        result["level"] = self.level
        result["ability_points"] = self.ability_points
        result["level_skills"] = self.level_skills

        result["base_skill_dict"] = {name : result.get_dict() for name, result in  self.base_skill_dict.items()}

        # クラスと内部値をタプルで保存する
        result["states"] = [(states.__class__.__name__, result.get_dict()) for states, result in zip(self.states, self.states)]

        return result

    def restore_from_dict(self, result):

        self.hp = result["hp"]
        self.base_max_hp = result["max_hp"]
 
        self.base_strength = result["strength"]
        self.base_dexterity = result["dexterity"]
        self.base_intelligence = result["intelligence"]
        self.unarmed = result["unarmed"]

        self.base_defense = result["defense"]
        self.base_evasion = result["evasion"]
        self.attack_speed = result["attack_speed"]

        self.xp_reward = result["xp_reward"]
        self.current_xp = result["current_xp"]
        self.level = result["level"]
        self.ability_points = result["ability_points"]
        self.level_skills = result["level_skills"]

        # クラスと内部値を結合する
        for s, r in result["states"]:
            if s:
                print(s, r)
                sd = eval(s)()
                sd.restore_from_dict(r)
                self._states.append(sd)

        for s, r in result["base_skill_dict"].items():
            if s:
                print(s, r)
                sd = self.base_skill_dict[s]
                sd.restore_from_dict(r)
                print(sd)


    @property
    def skill_list(self):
        """levelsにあるスキルのレベル合計からスキルリストを作成する"""

        # TODO game_stateの状態でループするか決めたい
        if hasattr(self.owner, "equipment") and self.owner.equipment:
            _skill_list = list(self.owner.equipment.skill_level_sum)
            _skill_list = sorted(_skill_list, key=lambda x: x.level, reverse=True)
 
            return _skill_list


    @property
    def passive_skill(self):
        result =  [skill for skill in self.skill_list if Tag.passive in skill.tag if skill not in self.switch_off_skills]
        return result
    @property
    def active_skill(self):
        result =  [skill for skill in self.skill_list if Tag.active in skill.tag if skill not in self.switch_off_skills]
        return result
    @property
    def attack_skill(self):
        result =  [skill for skill in self.skill_list if Tag.weapon in skill.tag if skill not in self.switch_off_skills]
        return result
    @property
    # スイッチの切れたスキルのリストを作って、装備スプライトの表示判定に使う
    def switch_off_skills(self):
        result = [skill for skill in self.skill_list if skill.data["switch"] == False]
        return result
    @property
    def skill_weight_list(self):
        result = sorted(self.skill_list, key=lambda x: x.item_weight)
        return result

    
    @property
    def states(self):
        for states in self._states:
            if states and not isinstance(states, str):
                states.owner = self.owner

        return self._states
    



        

    # @property
    # def attack_speed(self):
    #     if self.data["weapon"]:
    #         return self.data["weapon"].speed
    #     else:
    #         return self._attack_speed


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
    def STR(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["STR"]

        return self.base_strength + bonus

    @property
    def DEX(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["DEX"]

        return self.base_dexterity + bonus

    @property
    def INT(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["INT"]

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

        return self.base_evasion + bonus + (self.DEX / 2)
    

    @property
    def attack_damage(self):
        # ダメージと属性をタプルのリストで返す
        result = []

        if self.skill_list is not None and self.attack_skill:
            for skill in self.attack_skill:
                max_d = skill.damage 
                level = skill.level
                attr = skill.attr
                
                result.append((dice(1 + level//3, max_d+(self.STR//3)), attr))
        

        
        # if self.data["weapon"]:
        #     max_d = self.data["weapon"].damage
        #     level = self.data["weapon"].level
        #     attr = self.data["weapon"].attr
        else:
            max_d = self.unarmed["damage"]
            level = self.unarmed["level"]
            attr = self.unarmed["attr"]
            result.append((dice(1 + level//3, max_d+(self.STR//3)), attr))


        # result = [(dice(1 + level//3, max_d+(self.STR//3)), attr)]

        return result



    def hit_chance(self, target):
        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        hit = None

        if self.data["weapon"]:
            hit = self.data["weapon"].hit_rate
        else:
            hit = self.unarmed["hit_rate"]


        hit_chance = ((hit+self.DEX) / 100) * \
            (1 - (target.fighter.evasion / 100)) * 100
        print(f"{hit_chance=}")

        return hit_chance

    def change_hp(self, value, attr=None):
        results = []

        if attr == None:#回復効果などは属性なしとする
            results.append({"damage_pop": self.owner, "damage": value})
            return results


        if isinstance(value, str):# 完全防御やミスなど
            results.append({"damage_pop": self.owner, "damage": value})
            return results


        if self.resist[attr] <= 0:
            damage = int(value * 2.5)# 弱点ダメージ
        else:
            damage = int(value / self.resist[attr])

        self.hp += damage

        if self.hp <= 0:#死亡
            self.owner.blocks = False
            self.owner.is_dead = True
            results.append({"dead": self.owner})
            print(f"{self.owner.name} is dead x!")

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        results.append({"damage_pop": self.owner, "damage": damage})

        return results

    @stop_watch
    def attack(self, target, ranged=None):
        """attack_damage関数は属性ダメージをタプルのリストでここに返す
            ここでそのリストをループし、change_hp関数に渡す"""
        results = []
        

        for amount, attr in self.attack_damage:

        # damage = None

            # damage = self.attack_damage[0]
            # attack_attr = self.attack_damage[1]

            if ranged:# 遠隔
                attr = ranged.attr
                if random.randrange(1, 100) <= self.hit_chance(target):
                    if attr == "physical":
                        damage = dice(1 + ranged.level//3, ranged.damage+(self.DEX//3)) // target.fighter.defense
                    else:
                        damage = amount

                    # 完全防御
                    if not damage:
                        results.append(
                            {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no damage"})
                        results.extend(target.fighter.change_hp("Guard!"))
                        return results

                    if random.randrange(1, (100-self.DEX)) < 5:
                        damage *= 2# クリティカルdmg
                        results.append({"message": f"{self.owner.name.capitalize()} attack is critical HIT!"})

            else:
                if random.randrange(1, 100) <= self.hit_chance(target):
                    if attr == "physical":
                        damage = amount // target.fighter.defense
                    else:
                        damage = amount

                    # 完全防御
                    if not damage:
                        results.append(
                            {"message": f"{self.owner.name.capitalize()} attacks {target.name} but no damage"})
                        results.extend(target.fighter.change_hp("Guard!"))
                        return results


                    if random.randrange(1, (100-self.DEX)) < 5:
                        damage *= 2# クリティカルdmg
                        results.append({"message": f"{self.owner.name.capitalize()} attack is critical HIT!"})


            if amount:
                    # damage表示メッセージを格納する

                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} for {str(amount)} hit points."})
                results.extend(target.fighter.change_hp(-amount, attr))



            else:#回避
                results.append(
                    {"message": f"{self.owner.name.capitalize()} attacks {target.name} Avoided"})
                results.extend(target.fighter.change_hp("MISS"))


        return results
