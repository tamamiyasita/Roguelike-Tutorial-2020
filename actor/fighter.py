from actor.states.poison_status import PoisonStatus
import random
from constants import *
from util import dice, stop_watch, result_add
from actor.actor_set import *
from collections import Counter
import math
from actor.skills.base_skill import BaseSkill
from hit_anime import hit_particle, Hit_Anime


class Fighter:
    def __init__(self, hp=0, defense=0, STR=0, DEX=0, INT=0, attack_speed=DEFAULT_ATTACK_SPEED,
                 evasion=0, xp_reward=0, current_xp=0, level=1,
                 resist={"physical": 1, "fire": 1, "ice": 1, "lightning":1, "acid": 1, "poison": 1, "mind": 1}, ability_points=0):
        self.hp = hp
        self.base_max_hp = self.hp

        self.base_strength = STR
        self.base_dexterity = DEX
        self.base_intelligence = INT

        # self.unarmed = BaseSkill()#{"damage":1, "level":1, "attr":"physical"}

        self.base_defense = defense
        self.base_evasion = evasion
        self.attack_speed = attack_speed
        self.data = {}
        self.resist = resist

        self.owner = None
        self.xp_reward = xp_reward
        self.current_xp = current_xp
        self.level = level
        self.ability_points = ability_points
        self._states = arcade.SpriteList()

        self.level_skills = {}#level_upなどに伴う追加Skillの合計に使う
        self.base_skill_dict = skill_dict
        self._skill_list = arcade.SpriteList()
        self.equip_position = {0:(9,2), 1:(-9,3), 2:(9,-4), 3:(-11, -5), 4:(-14, 1),12:(0, 0)}

        # TODO バフデバフ効果に使う辞書　effect_bonus_update関数を作らねば
        self.effect_bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}


    def get_dict(self):
        result = {}

        result["hp"] = self.hp
        result["max_hp"] = self.base_max_hp

        result["strength"] = self.base_strength
        result["dexterity"] = self.base_dexterity
        result["intelligence"] = self.base_intelligence

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
    def unarmed(self):
        return self.owner.unarmed

    @property
    def skill_list(self):
        """levelsにあるスキルのレベル合計からスキルリストを作成する"""

        # TODO game_stateの状態でループするか決めたい
        if hasattr(self.owner, "equipment") and self.owner.equipment:
            _skill_list = list(self.owner.equipment.skill_list)
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
        try:
            result =  [skill for skill in self.skill_list if Tag.weapon in skill.tag if skill not in self.switch_off_skills]
            if not result:
                result = [self.unarmed]
        except:
            result = [self.unarmed]
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
    

    @property
    def max_hp(self):
        bonus = 0

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.states_bonus["max_hp"]

        return self.base_max_hp + bonus


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
    


    def effect_hit_chance(self, effect):
        attr = effect.attr
        resist = self.resist.get(attr)
        if resist:
            hit_chance = 100/resist
            if random.randrange(1, 100) <= hit_chance:
                self.states.append(effect)
        else:
            self.states.append(effect)


    def states_process(self, effect):
        pass

    def skill_process(self, skill):
        self.owner.state = state.DEFENSE
        
        message = ""
        results = []
        owner_name = self.owner.name.capitalize()
        skill_name = skill.name

        level = skill.level
        damage = skill.damage
        attr = skill.attr
        hit_rate = skill.hit_rate
        effect = skill.effect

        damage = dice(level, damage)

        # HP回復
        if attr == "recovery":
            results.append({"damage_pop": self.owner, "damage": damage, "message": f"has recovered {damage}HP"})
            self.hp += damage
            # 超過処理
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            return results

        # (命中率)％ ＝（α／１００）＊（１ー （β ／ １００））＊ １００
        # 命中率（α）＝９５、回避率（β）＝５
        hit_chance = ((hit_rate-self.DEX) / 100) * (1 - (self.evasion / 100)) * 100
        if random.randrange(1, 100) <= hit_chance:
            # ヒット 
            message = f"The {skill_name} hit"

            if effect:
                self.effect_hit_chance(effect)

            # critical_flag:
            if random.randrange(1, (100+self.DEX)) < 5:
                damage = skill.damage * 2
                message += " CRITICAL!"

            # 物理防御処理
            elif attr == "physical":
                damage = damage / self.defense


            if self.resist[attr] <= 0:
                damage *= 2.5# 弱点ダメージ
            else:
                damage = damage / self.resist[attr]


            # 完全防御
            if damage < 1:
                message += f" But {owner_name} was undamaged."
                results.extend([{"message": message},{"damage_pop": self.owner, "damage": "Guard!"}])
                return results

            
            else:
                if hasattr(skill, "anime"):
                    Hit_Anime(skill.anime, self.owner.position)
                hit_particle(target=self.owner)
                message += f" {owner_name} took {int(damage)} damage!"
                results.append({"message": message})


            damage = int(damage)

            results.extend(self.change_hp(damage))



        else:
            # 回避
            results.append({"damage_pop": self.owner, "damage": "MISS"})
            results.append({"message": f"{owner_name} Avoided {skill_name}"})

        return results

    def change_hp(self, damage):
        results = []

        self.hp -= damage

        # 死亡処理
        if self.hp <= 0 and self.owner.is_dead == False:
            self.owner.is_dead = True
            self.owner.blocks = False
            results.append({"dead": self.owner})

            print(f"{self.owner.name} is dead x!")

        results.append({"damage_pop": self.owner, "damage": -damage})

        return results

    @stop_watch
    def attack(self, target):
        """ここはダンプアタックを処理する
            attack_skillをループしskill_process関数に渡す"""
        results = []

        results.append({"message": f"{self.owner.name.capitalize()} attacked {target.name}"})
        for skill in self.attack_skill:

                results.extend(target.fighter.skill_process(skill))

        return results
